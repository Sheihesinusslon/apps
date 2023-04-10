# pylint: skip-file
from typing import Protocol


class IWhackyBot(Protocol):
    """Protocol class to define a basic interface for an adapter for any library providing interface for Telegram bot"""

    START: str = "start"
    HELP: str = "help"
    URBAN: str = "urban"
    GPT: str = "gpt"

    def welcome(self, *args, **kwargs) -> None:
        """Method to greet a user"""
        ...

    def handle_text_messages(self, *args, **kwargs) -> None:
        """Method to process text prompt from a user"""
        ...

    def handle_keyboard_messages(self, *args, **kwargs) -> None:
        """Method to process keyboards prompt from a user"""
        ...

    def handle_gpt_request(self, *args, **kwargs) -> None:
        """Method to redirect a user prompt to chat gpt"""
        ...

    def handle_ud_request(self, *args, **kwargs) -> None:
        """Method to redirect a user prompt to Urban Dict service"""
        ...

    def run_bot(self, *args, **kwargs) -> None:
        """Method to start a bot"""
        ...
