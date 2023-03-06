from typing import Protocol, Optional

from app.config import GREETING_VOICE, WELCOME_STICKER
from app.services.openai import GPT
from app.services.urban_dict import UrbanDict
from app.utils import greeting, CallBackData, Bot, Keyboard


class WhackyBot(Protocol):
    """Protocol class to define a basic interface for a telegram bot."""
    bot: Bot
    keyboard_manager: Keyboard

    def welcome(self) -> None:
        """Method to greet a user"""
        ...

    def handle_text_messages(self) -> None:
        """Method to process text prompt from a user"""
        ...

    def handle_keyboard_messages(self) -> None:
        """Method to process keyboards prompt from a user"""
        ...

    def run_bot(self) -> None:
        """Method to start a bot"""
        ...


class WhackyTeleBot:
    """Bot class to operate on TeleBot library API."""

    # All currently supported bot commands
    START = "start"
    HELP = "help"
    URBAN = "urban"
    GPT = "gpt"

    def __init__(self, bot: Bot, keyboard_manager: Keyboard):
        self.bot = bot
        self.keyboard_manager = keyboard_manager
        self._urban_dict: Optional[UrbanDict] = None
        self._gpt: Optional[GPT] = None

    def welcome(self, message) -> None:
        """Sends a welcome sticker and a voice message to greet a user"""
        self.bot.send_sticker(message.chat.id, WELCOME_STICKER)
        msg = greeting()
        keyboard = self.keyboard_manager.start_keyboard() if message.chat.type == "private" else None
        self.bot.send_message(message.chat.id, msg, reply_markup=keyboard)

    def handle_text_messages(self, message) -> None:
        """Handles text messages from a user. Generates a random response to user messages, working as a proxy
            for chatGPT, and suggests a basic keyboard set for further work"""
        prompt = message.text.lower()
        response = self.gpt.generate_random_response(prompt)

        keyboard = self.keyboard_manager.start_keyboard() if message.chat.type == "private" else None
        self.bot.send_message(
            message.chat.id,
            response,
            reply_markup=keyboard,
            parse_mode="html",
        )

    def handle_ud_request(self, message) -> None:
        """Handles a user request to use Urban Dictionary service"""
        prompt = message.text.lower().lstrip(f"/{self.URBAN}").lstrip(self.URBAN)
        response = self.urban_dict.get_definitions(prompt)

        keyboard = self.keyboard_manager.start_keyboard() if message.chat.type == "private" else None
        self.bot.send_message(
            message.chat.id,
            response,
            reply_markup=keyboard,
            parse_mode="html",
        )

    def handle_gpt_request(self, message) -> None:
        """Handles a user request to use OpenAI service"""
        prompt = message.text.lower().lstrip(f"/{self.GPT}").lstrip(self.GPT)
        if not prompt:
            self._send_gpt_instruction(message)
        else:
            response = self.gpt.generate_response(prompt)

            keyboard = self.keyboard_manager.start_keyboard() if message.chat.type == "private" else None
            self.bot.send_message(
                message.chat.id,
                response,
                reply_markup=keyboard,
                parse_mode="html",
            )

    def handle_keyboard_messages(self, call) -> None:
        """Handles keyboard input from a user, providing instructions or another keyboard sets to continue working
            with user's prompt/request"""
        if call.data == CallBackData.URBAN:
            response = f"Send <b>{self.URBAN}</b> to get 10 random\nwords/phrases from Urban Dictionary\n\n"\
                  f"Send <b>{self.URBAN} 'your word/phrase'</b>\nto get Urban definition\n"

            self.bot.send_message(
                call.message.chat.id,
                response,
                parse_mode="html",
                reply_markup=self.keyboard_manager.start_keyboard(),
            )

        if call.data == CallBackData.HOROSCOPE:
            response = "Choose your patronus >>>"
            self.bot.send_message(
                call.message.chat.id,
                response,
                reply_markup=self.keyboard_manager.horoscope_keyword(),
            )

        if call.data == CallBackData.ZODIAC:
            response = self.gpt.get_horoscope()
            keyboard = self.keyboard_manager.start_keyboard() if call.message.chat.type == "private" else None
            self.bot.send_message(call.message.chat.id, response, reply_markup=keyboard)

        if call.data == CallBackData.HELLO:
            self.bot.send_sticker(call.message.chat.id, WELCOME_STICKER)
            with open(GREETING_VOICE, "rb") as voice:
                self.bot.send_voice(
                    call.message.chat.id,
                    voice=voice,
                    reply_markup=self.keyboard_manager.start_keyboard()
                )

        if call.data == CallBackData.GPT:
            message = call.message
            self._send_gpt_instruction(message)

    def run_bot(self) -> None:
        """Starts Telebot polling"""
        self.bot.polling(non_stop=True, interval=0)

    @property
    def urban_dict(self):
        """If not instantiated, creates a client to connect with Urban Dictionary service"""
        if not self._urban_dict:
            self._urban_dict = UrbanDict()
        return self._urban_dict

    @property
    def gpt(self):
        """If not instantiated, creates a client to connect with OpenAI service"""
        if not self._gpt:
            self._gpt = GPT()
        return self._gpt

    def _send_gpt_instruction(self, message):
        response = f"Send <b>{self.GPT}</b> and your question\nto send a request to ChatGPT\n\n"
        self.bot.send_message(
            message.chat.id,
            response,
            parse_mode="html",
            reply_markup=self.keyboard_manager.start_keyboard(),
        )
