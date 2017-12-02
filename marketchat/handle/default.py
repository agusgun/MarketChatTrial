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

      To view list of instructions, type "help"
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
            label='View Promos', data=make_beacon('promo'))
        ]))
  ])

  return True


__all__ = ['route']
