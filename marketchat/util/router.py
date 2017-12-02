from linebot.models import MessageEvent, PostbackEvent, TextMessage
from marketchat.util.beacon import parse_beacon


class Router:
    def __init__(self):
        self.__rules = []

    # Internal.

    def __decorator(func):
        return lambda self, cb=None, *args, **kwargs: (lambda cb: func(
            self, cb, *args, **kwargs)) if cb is None else func(self, cb, *args, **kwargs)

    # Administration.

    @__decorator
    def handle(self, cb):
        self.__rules.append(cb)

    @__decorator
    def handle_event(self, cb, event_type):
        self.handle(lambda e: cb(e) if isinstance(e, event_type) else False)

    @__decorator
    def handle_message_event(self, cb, message_type):
        self.handle_event(
            lambda e: cb(e) if isinstance(e.message, message_type) else False,
            event_type=MessageEvent)

    @__decorator
    def handle_text_message_event(self, cb, text):
        text = text.strip().lower()
        self.handle_message_event(
            lambda e: cb(e) if e.message.text.strip(
            ).lower() == text else False,
            message_type=TextMessage)

    @__decorator
    def handle_postback_event(self, cb, action):
        self.handle_event(
            lambda e: (lambda data: cb(e, data) if data.action == action else False)(
                parse_beacon(e.postback.data)),
            event_type=PostbackEvent)

    # Run.

    def __call__(self, event):
        for rule in self.__rules:
            if rule(event):
                return True
        # No handler.
        return False
