from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from marketchat.db import catalog
from textwrap import dedent

route = Router()


@route.handle_postback_event(action="view_stores")
def handle_view_stores(event, data):
  i_stores = enumerate(catalog.stores)

  bot_api.reply_message(event.reply_token, TemplateSendMessage(
    alt_text="Available store list", template=ButtonsTemplate(
      title="Available store", text="Choose store:", actions=[
        PostbackTemplateAction(label=store, data=make_beacon(
          'view', store=i)) for i, store in i_stores
      ])))

  return True


@route.handle_postback_event(action="view_categories")
def handle_view_categories(event, data):
  i_categories = enumerate(catalog.categories)

  bot_api.reply_message(event.reply_token, TemplateSendMessage(
    alt_text="Available category list", template=ButtonsTemplate(
      title="Available category", text="Choose category:", actions=[
        PostbackTemplateAction(label=category, data=make_beacon(
          'view', category=i)) for i, category in i_categories
      ])))

  return True


__all__ = ['route']
