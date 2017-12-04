from linebot.models import Postback, PostbackEvent, TextMessage, TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.db import catalog
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router, main_router, overlay_router
from .view import view_catalog

route = Router()


# Search by items.

item_overlay = Router()


@item_overlay.handle_message_event(message_type=TextMessage)
def handle_item_overlay_message(event):
    i_items = enumerate(catalog.items)

    text = event.message.text.strip().lower()
    i_data = [(i, item)
              for i, item in i_items if text in item.strip().lower()]

    if len(i_data) == 1:
        i, item = i_data[0]
        view_catalog(event, item=i)

        overlay_router(event, None)
    else:
        bot_api.reply_message(event.reply_token,
                              TextSendMessage(text=(("""
You specified ambiguous keyword.

Matched item:
""" + "\n".join(f"- {name}" for i, name in i_data) + """

Type full name of the item to proceed.
""") if len(i_data) > 1 else """
No item matches with specified keyword.
""").strip()))

    return True


# Stores.

@route.handle_postback_event(action="view_stores")
def handle_view_stores(event, data):
    i_stores = enumerate(catalog.stores)

    overlay_router(event, item_overlay)

    bot_api.reply_message(event.reply_token, [
        TemplateSendMessage(
            alt_text="Available store list", template=ButtonsTemplate(
                title="Available store", text="Choose store:", actions=[
                    PostbackTemplateAction(label=store, data=make_beacon(
                        'view', store=i)) for i, store in i_stores
                ])),

        TextSendMessage(text="""
You can also type the store name.
""".strip())
    ])

    return True


# Category.

@route.handle_postback_event(action="view_categories")
def handle_view_categories(event, data):
    i_categories = enumerate(catalog.categories)

    overlay_router(event, item_overlay)

    bot_api.reply_message(event.reply_token, [
        TemplateSendMessage(
            alt_text="Available category list", template=ButtonsTemplate(
                title="Available category", text="Choose category:", actions=[
                    PostbackTemplateAction(label=category, data=make_beacon(
                        'view', category=i)) for i, category in i_categories
                ])),

        TextSendMessage(text="""
You can also type the category name.
""".strip())
    ])

    return True


__all__ = ['route']
