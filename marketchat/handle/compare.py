from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from marketchat.db import catalog

route = Router()


@route.handle_postback_event(action="compare")
def handle_compare(event, data):
    a, b = [catalog.items[int(i)] for i in data.params['id']]

    bot_api.reply_message(event.reply_token, TextSendMessage(text=f"""
{a.name} (1) vs {b.name} (2)

Price:
(1) Rp {'{:,}'.format(a.price)},-{f" ({round(a.promo * 100)}% off)" if a.promo is not None else ""}
(2) Rp {'{:,}'.format(b.price)},-{f" ({round(b.promo * 100)}% off)" if b.promo is not None else ""}
Difference: Rp {'{:,}'.format(abs(a.price - b.price))},-

Store:
(1) {a.store}
(2) {b.store}
""".strip()))

    return True


__all__ = ['route']
