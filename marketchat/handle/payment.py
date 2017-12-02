from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
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




__all__ = ['route']
