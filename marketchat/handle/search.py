from linebot.models import Postback, PostbackEvent, TextMessage, TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.db import catalog
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router, main_router, overlay_router
from .view import view_catalog

route = Router()


# Stores.

store_overlay = Router()


@store_overlay.handle_message_event(message_type=TextMessage)
def handle_store_overlay_message(event):
    i_stores = enumerate(catalog.stores)

    text = event.message.text.strip().lower()
    i_data = [(i, store)
              for i, store in i_stores if text in store.strip().lower()]

    if len(i_data) == 1:
        i, store = i_data[0]
        view_catalog(event, store=i)

        overlay_router(event, None)
    else:
        bot_api.reply_message(event.reply_token,
                              TextSendMessage(text=(("""
You specified ambiguous keyword.

Matched store:
""" + "\n".join(f"- {name}" for i, name in i_data) + """

Type full name of the store to proceed.
""") if len(i_data) > 1 else """
No store matches with specified keyword.
""").strip()))

    return True


@route.handle_postback_event(action="view_stores")
def handle_view_stores(event, data):
    i_stores = enumerate(catalog.stores)

    overlay_router(event, store_overlay)

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

category_overlay = Router()


@category_overlay.handle_message_event(message_type=TextMessage)
def handle_category_overlay_message(event):
    i_categories = enumerate(catalog.categories)

    text = event.message.text.strip().lower()
    i_data = [(i, category)
              for i, category in i_categories if text in category.strip().lower()]

    if len(i_data) == 1:
        i, category = i_data[0]
        view_catalog(event, category=i)

        overlay_router(event, None)
    else:
        bot_api.reply_message(event.reply_token,
                              TextSendMessage(text=(("""
You specified ambiguous keyword.

Matched category:
""" + "\n".join(f"- {name}" for i, name in i_data) + """

Type full name of the category to proceed.
""") if len(i_data) > 1 else """
No category matches with specified keyword.
""").strip()))

    return True


@route.handle_postback_event(action="view_categories")
def handle_view_categories(event, data):
    i_categories = enumerate(catalog.categories)

    overlay_router(event, category_overlay)

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
