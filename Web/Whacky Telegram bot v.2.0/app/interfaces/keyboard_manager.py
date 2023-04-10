# pylint: skip-file
from typing import Protocol


class IKeyboardManager(Protocol):
    """Interface for KeyboardManager instance"""

    def start_keyboard(self, *args, **kwargs):
        ...

    def horoscope_keyboard(self, *args, **kwargs):
        ...

    def get_default_keyboard(self, *args, **kwargs):
        ...
