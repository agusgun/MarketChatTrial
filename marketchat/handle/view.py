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

    if 'store' in data.params:
        store = catalog.stores[int(data.params['store'])]
        i_items = [(i, item) for i, item in i_items if store == item.store]
    if 'category' in data.params:
        category = catalog.categories[int(data.params['category'])]
        i_items = [(i, item)
                   for i, item in i_items if category == item.category]
    if 'compare' in data.params:
        compare = int(data.params['compare'])
        i_items = [(i, item) for i, item in i_items if compare != i]
    if 'promo' in data.params:
        i_items = [(i, item) for i, item in i_items if item.promo is not None]
    if 'popular' in data.params:
        i_items = [(i, item) for i, item in i_items if item.flags &
                   catalog.ItemFlag.POPULAR]

    # Presentation.

    bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='Product list', template=CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url=item.image, text='Rp ' + str(item.price), title=item.name,
                actions=[
                    PostbackTemplateAction(
                        label='Select', data=make_beacon(
                            'compare', id=[data.params['compare'], i])),
                ] if 'compare' in data.params else [
                    PostbackTemplateAction(
                        label='Buy', data=make_beacon('buy', id=i)),
                    PostbackTemplateAction(
                        label='Details', data=make_beacon('details', id=i)),
                    PostbackTemplateAction(
                        label='Compare', data=make_beacon('view', compare=i))
                ]) for i, item in i_items])))

    return True


@route.handle_postback_event(action="details")
def handle_detail(event, data):
    item = catalog.items[int(data.params['id'])]

    bot_api.reply_message(event.reply_token, TextSendMessage(
        text=dedent(f"""
            {item.name}

            Price: Rp {item.price}
            Store: {item.store}
        """).strip()))

    return True


__all__ = ['route']
