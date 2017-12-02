from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
from marketchat.handle import route
from marketchat.util.line_bot import bot_api, handler
from textwrap import dedent

app = Flask(__name__)


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value.
    signature = request.headers['X-Line-Signature']

    # Get request body as text.
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body.
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.default()
def handle_default(event):
    if not route(event):
        bot_api.reply_message(event.reply_token, TextSendMessage(text=dedent("""
            Need help?

            You can scroll up and select an option from the menus/cards shown previously.
            You can also view the main menu by typing "menu".
        """).strip()))


__all__ = ['app']
