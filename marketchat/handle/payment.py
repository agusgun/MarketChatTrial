from linebot.models import TextMessage, VideoMessage, ImageMessage, TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router, overlay_router
from marketchat.db import catalog
from textwrap import dedent

route = Router()


@route.handle_postback_event(action="buy")
def handle_buy_product(event, data):
    bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='Payment Method', template=ButtonsTemplate(
            title='Payment Method?', text='Choose method:', actions=[
                PostbackTemplateAction(
                    label='Payment by Transfer', data=make_beacon('transfer', itemId=1)),
                PostbackTemplateAction(
                    label='Payment by COD', data=make_beacon('cod', itemId=1))
            ])))

    return True


@route.handle_postback_event(action="transfer")
def handle_transfer(event, data):
    bot_api.reply_message(event.reply_token, TextSendMessage(text=dedent("""
            Seller status verdict are safe.\nSeller name and account\'s number are: Toko Yoyo-*900-00-123-123*. Bank name: Mandiri\nTransfer payment is guaranteed to be safe.\nIf you have any dificulty in the payment please contact our administrator: +62818885.\n\nType "validate" to validate your transfer
        """).strip()))

    return True


@route.handle_postback_event(action="cod")
def handle_cod(event, data):
    bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='Payment COD', template=ButtonsTemplate(
            title='When?', text='Choose schedule:', actions=[
                PostbackTemplateAction(
                    label='30 Nov 08.00-Marina', data=make_beacon('choosecod', itemId=1)),
                PostbackTemplateAction(
                    label='20 Dec 19.00-Sydney', data=make_beacon('choosecod', itemId=2))
            ])))

    return True


@route.handle_postback_event(action="choosecod")
def handle_choose_cod(event, data):
    bot_api.reply_message(event.reply_token, TextSendMessage(text=dedent("""
            Your seller has been contacted by our system. Please meet your seller at the meeting point on time.\nSeller name: Toko Yoyo. Seller contact: +6281-222-333-444
        """).strip()))

    return True


validate_overlay = Router()


@validate_overlay.handle_message_event(message_type=ImageMessage)
def handle_validate_overlay_message(event):
    bot_api.reply_message(event.reply_token,
                          TextSendMessage(text=dedent("""
            The system already validate your evidence of transfer.\nYour transfer are accepted by our system.\nOur system already contacted the seller. You can check the status of your order.
        """).strip()))

    return True


@validate_overlay.handle_message_event(message_type=VideoMessage)
def handle_validate_overlay_message(event):
    bot_api.reply_message(event.reply_token,
                          TextSendMessage(text=dedent("""
            The system already validate your evidence of transfer.\nYour transfer are not accepted by our system.\nPlease upload your evidence of transfer again.
        """).strip()))

    return True


@route.handle_message_event(message_type=TextMessage)
def handle_validate_message(event):
    text = event.message.text.strip().lower()

    if (text == 'validate'):
        overlay_router(event, validate_overlay)
        bot_api.reply_message(event.reply_token,
                              TextSendMessage(text=dedent("""
                Please upload your evidence of transfer.
            """).strip()))
    else:
        bot_api.reply_message(event.reply_token, TextSendMessage(text=dedent("""
            Need help?

            You can scroll up and select an option from the menus/cards shown previously.
            You can also view the main menu by typing "menu".
        """).strip()))

    return True


__all__ = ['route']
