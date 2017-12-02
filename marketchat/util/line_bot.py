from linebot import LineBotApi, WebhookHandler
import sys
import os

channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

__all__ = ['bot_api', 'handler']
