from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from marketchat.db import catalog
from textwrap import dedent

route = Router()


@route.handle_postback_event(action="special_deals")
def handle_special_deals(event, data):
    bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='Special deals menu', template=ButtonsTemplate(
            title='What do you want to do?', text='Choose action:', actions=[
                PostbackTemplateAction(
                    label='Promo Items', data=make_beacon('view', promo=1)),
                PostbackTemplateAction(
                    label='Recommended Items', data=make_beacon('unimplemented')),
                PostbackTemplateAction(
                    label='Popular Items', data=make_beacon('view', popular=1))
            ])))

    return True


__all__ = ['route']
