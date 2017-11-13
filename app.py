# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import errno
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    cancel_message = 'type "cancel" to cancel search'
    if text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='Status message: ' + profile.status_message
                    )
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't leave from 1:1 chat"))
    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'imagemap':
        pass
    elif text == 'Find egg':
        carousel_template = CarouselTemplate(columns=[
          CarouselColumn(text='Rp 25.000,-', title='Arabian Egg', actions=[
            PostbackTemplateAction(label='Buy', data='buy_a'),
            PostbackTemplateAction(label='Details', data='details_a'),
            PostbackTemplateAction(label='Compare', data='compare')
          ]),
          CarouselColumn(text='Rp 25.000,-', title='Australian Egg', actions=[
            PostbackTemplateAction(label='Buy', data='buy_b'),
            PostbackTemplateAction(label='Details', data='details_b'),
            PostbackTemplateAction(label='Compare', data='compare')
          ])
        ])
        template_message = TemplateSendMessage(
          alt_text='Carousel alt text', template=carousel_template)
        bot_api.reply_message(reply_token, template_message)
    elif text == 'cancel':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="Welcome..."))
    elif text == 'category':
        buttons_template = ButtonsTemplate(
            title='In what category?', text='Choose category:', actions=[
            PostbackTemplateAction(label='Grocery', data='grocery'),
            PostbackTemplateAction(label='Fashion', data='fashion')
        ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'details_a':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Arabian egg\n\nPrice: Rp. 25,000.00\nStore location: Yogya Karapitan (Bandung)\nCondition: Good'))
    elif text == 'details_b':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Australian egg\n\nPrice: Rp. 25,000.00\nStore location: Yogya Riau Junction (Bandung)\nCondition: Good'))
    elif text == 'grocery':
        carousel_template = CarouselTemplate(columns=[
          CarouselColumn(text='Rp 25.000,-', title='Arabian Egg', actions=[
            PostbackTemplateAction(label='Buy', data='buy_a'),
            PostbackTemplateAction(label='Details', data='details_a'),
            PostbackTemplateAction(label='Compare', data='compare')
          ]),
          CarouselColumn(text='Rp 25.000,-', title='Australian Egg', actions=[
            PostbackTemplateAction(label='Buy', data='buy_b'),
            PostbackTemplateAction(label='Details', data='details_b'),
            PostbackTemplateAction(label='Compare', data='compare')
          ])
        ])
        template_message = TemplateSendMessage(
          alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(reply_token, template_message)
    elif text == 'Choose Arabian egg':
        message = 'Arabian egg\n\nPrice: Rp. 25,000.00\nStore location: Yogya karapitan (Bandung)\nCondition: Good\n\nTo buy this product type "Buy Arabian egg"'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
    elif text == 'Findstore Yogya':
        message = 'Search result for "Yogya"\n1. Yogya Karapitan\n2. Yogya Riau Junction\n3. Yogya Sunda\n4. Yogya Minimarket\n\nType number to choose shope e.g: 1 to choose Yogya Karapitan'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
    elif text == '1':
        message = 'You choose Yogya Karapitan\n\nTo search products, type "Find <product name>\n\nTo view other instructions type "help"'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
    elif text == 'list transactions':
        #Actionnya belum bisa nanti actionnya ke view transaction 15022 aja
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://www.theurbanlist.com/content/article/wysiwyg/three-williams-eggs.png',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date')),
            ImageCarouselColumn(image_url='https://www.fritzmag.com.au/wp-content/uploads/2016/12/Get-Your-Googie-On-With-South-Australian-Eggs-2.jpg',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'view transaction 15022':
        #Edit aja gambarnya + actionnya juga + labelnya juga masih dummy ini
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://www.theurbanlist.com/content/article/wysiwyg/three-williams-eggs.png',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date')),
        ])
    elif text == 'Compare':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'Display all':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="Arabian egg vs Mysterious egg"))
    elif text == 'Change':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == '1':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == '2':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'recommend':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'promo':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'Recommend by history':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'Any popular products right now?':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'Trending products':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'Buy Arabian egg':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='You can choose between two payment methods.\n\nPayment by transfer\nif you want to pay using transfer method please type "pay by transfer"\n\nPayment by COD (Cash On Delivery)\nif you want to pay using Cash On Delivery method please type "pay by COD"'))
    elif text == 'pay by transfer':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='Here\'s your seller account number: 900-00-123-123\n\nYour seller are certified seller'))
    elif text == 'pay by COD':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='Here is the list of your seller schedule and meeting point.\n\n1. 30 November 2017 08.00 - Marina Bay\n2. 1 Desember 2017 19.00 - Sydney Opera House\n\nPlease choose one from the list by typing "choose #number". The number is the number from the list, e.g "choose 1"'))
    elif text == 'choose 1':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='Your seller has been contacted by our system. Please meet your seller at the meeting point on time.'))
    elif text == 'validate transfer':
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='Please upload your evidence of transfer.'))
    else:
        default_message='Welcome to MarketChat\n\nTo search products, type "Find egg" e.g. Find egg\n\nTo cancel search, type "cancel"\n\nTo view other instructions, type"help"\n\nWhat can i do for you?'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=default_message))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message = 'The system already validate your evidence of transfer.\nYour transfer are accepted by our system. Our system already contacted the seller. You can check the status of your order.\nPlease type "help" to know the command for status of your order'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
        message = 'The system already validate your evidence of transfer.\nYour transfer are not accepted by our system.\nPlease validate your transfer again.'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))    
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Received other message type, ext=' + ext),
        ])

@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Received a file.'),
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)