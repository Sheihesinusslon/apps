from typing import Protocol, Any


# pylint: skip-file


class ITeleKeyboard(Protocol):
    """Interface for Telebot Keyboard instance"""

    keyboard: Any

    def add(self, *args, **kwargs):
        ...


class ITeleButton(Protocol):
    """Interface for Telebot Button instance"""

    def __init__(self, *args, **kwargs):
        ...

    def __call__(self, *args, **kwargs):
        ...
