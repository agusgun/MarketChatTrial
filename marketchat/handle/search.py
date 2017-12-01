from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import encode_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from textwrap import dedent

route = Router()


@route.handle_postback_event(action="search")
def handle_search(event, beacon):
  bot_api.reply_message(event.reply_token, TemplateSendMessage(
    alt_text='Product list', template=CarouselTemplate(columns=[
      CarouselColumn(thumbnail_image_url='https://matriposterous.files.wordpress.com/2010/11/image_298.jpg',text='Rp 25.000,-', title='Arabian Egg', actions=[
        PostbackTemplateAction(
          label='Buy', data=encode_beacon('buy')),
        PostbackTemplateAction(
          label='Details', data=encode_beacon('details_a')),
        PostbackTemplateAction(
          label='Compare', data=encode_beacon('compare'))
      ]),
      CarouselColumn(thumbnail_image_url='https://22251-presscdn-pagely.netdna-ssl.com/wp-content/uploads/2015/09/1401323431993.jpg',text='Rp 25.000,-', title='Australian Egg', actions=[
        PostbackTemplateAction(
          label='Buy', data=encode_beacon('buy')),
        PostbackTemplateAction(
          label='Details', data=encode_beacon('details_b')),
        PostbackTemplateAction(
          label='Compare', data=encode_beacon('compare'))
      ])
    ]))
  )
  return True


__all__ = ['route']
