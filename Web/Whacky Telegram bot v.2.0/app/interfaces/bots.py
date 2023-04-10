# pylint: skip-file
from typing import Protocol


class ITeleBot(Protocol):
    """Interface for Telebot bot instance"""

    def send_message(self, *args, **kwargs):
        ...

    def send_sticker(self, *args, **kwargs):
        ...

    def send_voice(self, *args, **kwargs):
        ...

    def message_handler(self, *args, **kwargs):
        ...

    def callback_query_handler(self, *args, **kwargs):
        ...

    def polling(self, *args, **kwargs):
        ...
