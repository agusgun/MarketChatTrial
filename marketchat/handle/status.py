from linebot.models import TextSendMessage, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from marketchat.util.beacon import make_beacon
from marketchat.util.line_bot import bot_api
from marketchat.util.router import Router
from marketchat.db import catalog

route = Router()


@route.handle_postback_event(action="status")
def handle_status(event, data):
    i_statuses = enumerate(catalog.statuses)

    bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text="Active transactions list", template=ButtonsTemplate(
            title="Active transactions", text="Choose transaction:", actions=[
                PostbackTemplateAction(label=f"ID#{i} Jeans AX", data=make_beacon(
                    'status_detail', id=i)) for i, status in i_statuses
            ])))

    return True


@route.handle_postback_event(action="status_detail")
def handle_status_detail(event, data):
    status_id = int(data.params['id'])
    status = catalog.statuses[status_id]

    bot_api.reply_message(event.reply_token, TextSendMessage(text=f"""
Transaction #{status_id}

Item: {status.item.name}
Price: {status.item.price}
Store: {status.item.store}

Status: {status.status}
""".strip()))

    return True


__all__ = ['route']
