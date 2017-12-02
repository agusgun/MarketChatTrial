from linebot.models import TextMessage, TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router, overlay_router
from marketchat.db import catalog
from textwrap import dedent

route = Router()


# Stores.

store_overlay = Router()

@store_overlay.handle_message_event(message_type=TextMessage)
def handle_store_overlay_message(event):
    text = event.message.text.strip().lower()
    data = [store for store in catalog.stores if text in store.strip().lower()]

    if len(data) == 1:
        event = None
    else:
        bot_api.reply_message(event.reply_token,
            TextSendMessage(text=(dedent("""
                You specified ambiguous keyword.

                Matched store:
            """) + "\n".join(f"- {name}" for name in data) + dedent("""

                Type full name of the store to proceed.
            """)) if len(data) > 1 else dedent("""
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

        TextSendMessage(text=dedent("""
            You can also type the store name.
        """).strip())
    ])

    return True


# Category.

category_overlay = Router()

@category_overlay.handle_message_event(message_type=TextMessage)
def handle_category_overlay_message(event):
    text = event.message.text.strip().lower()

    bot_api.reply_message(event.reply_token,
        TextSendMessage(text=dedent("""
            ehehehehehehehehe oc
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

        TextSendMessage(text=dedent("""
            You can also type the category name.
        """).strip())
    ])

    return True


__all__ = ['route']
