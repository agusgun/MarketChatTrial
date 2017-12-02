from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from marketchat.db import catalog
from textwrap import dedent

route = Router()


@route.handle_postback_event(action="compare")
def handle_compare(event, data):
    a, b = [catalog.items[i] for i in data.params['id']]

    bot_api.reply_message(event.reply_token, TextSendMessage(text=dedent(f"""
        {a.name} (1) vs {b.name} (2)

        Price:
        (1) Rp {a.price}
        (2) Rp {b.price}
        Difference: Rp {abs(a.price - b.price)}

        Store:
        (1) {a.store}
        (2) {b.store}
    """)))

    return True
