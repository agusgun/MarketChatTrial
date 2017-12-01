from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from marketchat.db import catalog
from textwrap import dedent

route = Router()


@route.handle_postback_event(action="view")
def handle_view(event, data):
  i_items = enumerate(catalog.items)

  # Filters.
  if 'store' in data:
    i_items = [(i, item) for i, item in i_items if catalog.stores[item.store] == data['store']]
  if 'category' in data:
    i_items = [(i, item) for i, item in i_items if catalog.categories[item.category] == data['category']]

  bot_api.reply_message(event.reply_token, TemplateSendMessage(
    alt_text='Product list', template=CarouselTemplate(columns=[
      CarouselColumn(
        thumbnail_image_url=item.image, text='Rp ' + str(item.price), title=item.name,
        actions=[
          PostbackTemplateAction(
            label='Buy', data=make_beacon('buy', id=i)),
          PostbackTemplateAction(
            label='Details', data=make_beacon('details', id=i)),
          PostbackTemplateAction(
            label='Compare', data=make_beacon('compare', id=i))
        ]) for i, item in i_items])))

  return True


__all__ = ['route']