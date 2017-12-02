from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from textwrap import dedent

route = Router()


@route.handle_text_message_event(text="menu")
def handle_menu(event):
    bot_api.reply_message(event.reply_token, [
        TextSendMessage(text=dedent("""
            Welcome to MarketChat!

            You can choose what you want to do on the menu below.
            Happy shopping! :D

            If you are lost, you can type "menu" to view the menu again.
        """).strip()),

        TemplateSendMessage(
            alt_text='Main menu', template=ButtonsTemplate(
                title='What do you want to do?', text='Choose action:', actions=[
                    PostbackTemplateAction(
                      label='Search Items', data=make_beacon('view_categories')),
                    PostbackTemplateAction(
                        label='Search Store', data=make_beacon('view_stores')),
                    PostbackTemplateAction(
                        label='View Transactions', data=make_beacon('status')),
                    PostbackTemplateAction(
                        label='Special Deals', data=make_beacon('special_deals'))
                ]))
    ])

    return True


__all__ = ['route']
