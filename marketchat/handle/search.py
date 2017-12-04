from linebot.models import Postback, PostbackEvent, TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.db import catalog
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router, main_router, overlay_router
from .view import text_overlay_route

route = Router()


# Stores.

@route.handle_postback_event(action="view_stores")
def handle_view_stores(event, data):
    i_stores = enumerate(catalog.stores)

    overlay_router(event, text_overlay_route)

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

    overlay_router(event, text_overlay_route)

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
