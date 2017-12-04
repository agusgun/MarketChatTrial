from linebot.models import TextMessage, TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from marketchat.db import catalog


def view_catalog(event, i_items, is_compare=False):
    bot_api.reply_message(event.reply_token, filter(None, [
        TextSendMessage(text="""
Select item to compare with:
""".strip()) if is_compare else None,
        TemplateSendMessage(
            alt_text='Product list', template=CarouselTemplate(columns=[
                CarouselColumn(
                    thumbnail_image_url=item.image, text='Rp ' + str(item.price), title=item.name,
                    actions=[
                        PostbackTemplateAction(
                            label='Select', data=make_beacon(
                                'compare', id=[is_compare, i])),
                    ] if is_compare else [
                        PostbackTemplateAction(
                            label='Buy', data=make_beacon('buy', id=i)),
                        PostbackTemplateAction(
                            label='Details', data=make_beacon('details', id=i)),
                        PostbackTemplateAction(
                            label='Compare', data=make_beacon('view', compare=i))
                    ]) for i, item in i_items]))
        ]))


# Overlay route.

text_overlay_route = Router()


@text_overlay_route.handle_message_event(message_type=TextMessage)
def handle_text_overlay_route_message(event):
    i_items = enumerate(catalog.items)

    text = event.message.text.strip().lower()
    i_items = [(i, item) for i, item in i_items if text in item.name.lower()]

    if len(i_items) > 0:
        view_catalog(event, i_items)
    else:
        bot_api.reply_message(event.reply_token, TextSendMessage(text="""
No item matches with specified keyword.
""".strip()))

    return True


# Routes.

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

    view_catalog(event, i_items, 'compare' in data.params)
    return True


@route.handle_postback_event(action="details")
def handle_detail(event, data):
    item = catalog.items[int(data.params['id'])]
    if (item.promo is not None):
        bot_api.reply_message(event.reply_token, TextSendMessage(
            text=f"""
            {item.name}

Price: Rp {item.price}
Store: {item.store}
Stock: {item.stock}
Disc: {item.promo*100}%
Delivery Cost: {item.deliv}
            """.strip()))
    else:
        bot_api.reply_message(event.reply_token, TextSendMessage(
            text=f"""
            {item.name}

Price: Rp {item.price}
Store: {item.store}
Stock: {item.stock}
Delivery Cost: {item.deliv}
            """.strip()))

    return True


__all__ = ['route', 'text_overlay_route']
