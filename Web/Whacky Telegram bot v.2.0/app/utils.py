from enum import Enum, auto
from random import choice
from typing import TypeVar, Any, Generic, Final

Bot = TypeVar("Bot")
Keyboard = TypeVar("Keyboard", bound=Any)
Button = TypeVar("Button", bound=Any)

PRIVATE_CHAT: Final[str] = "private"


class KeyboardManager(Generic[Keyboard, Button]):
    """Provides an interface to create different sets of Keyboards with Buttons"""
    def __init__(self, keyboard: Keyboard, button: Button):
        self.keyboard = keyboard
        self.button = button

    def start_keyboard(self) -> Keyboard:
        """The main inline keyboard that the bot is going to reply every time"""
        self.__clear_keyborad()
        # init keyboard and prepare keys
        key1 = self.button(text="Say Hello", callback_data=CallBackData.HELLO)
        key2 = self.button(text="Get a Horoscope for the day", callback_data=CallBackData.HOROSCOPE)
        key3 = self.button(text="Urban Dictionary", callback_data=CallBackData.URBAN)
        key4 = self.button(text="ChatGPT", callback_data=CallBackData.GPT)

        # add keys to the keyboard
        self.keyboard.add(key1)
        self.keyboard.add(key2)
        self.keyboard.add(key3)
        self.keyboard.add(key4)

        return self.keyboard

    def horoscope_keyword(self) -> Keyboard:
        """Prepare keys for inline keyboard, return keyboard"""
        # clear keyboard
        self.__clear_keyborad()
        # prepare keys
        key_aries = self.button(text="Aries", callback_data=CallBackData.ZODIAC)
        key_taurus = self.button(text="Taurus", callback_data=CallBackData.ZODIAC)
        key_gemini = self.button(text="Gemini", callback_data=CallBackData.ZODIAC)
        key_cancer = self.button(text="Cancer", callback_data=CallBackData.ZODIAC)
        key_leo = self.button(text="Leo", callback_data=CallBackData.ZODIAC)
        key_virgo = self.button(text="Virgo", callback_data=CallBackData.ZODIAC)
        key_libra = self.button(text="Libra", callback_data=CallBackData.ZODIAC)
        key_scorpio = self.button(text="Scorpio", callback_data=CallBackData.ZODIAC)
        key_sagittarius = self.button(text="Sagittarius", callback_data=CallBackData.ZODIAC)
        key_capricorn = self.button(text="Capricorn", callback_data=CallBackData.ZODIAC)
        key_aquarius = self.button(text="Aquarius", callback_data=CallBackData.ZODIAC)
        key_pisces = self.button(text="Pisces", callback_data=CallBackData.ZODIAC)

        # add keys to keyboard
        self.keyboard.add(key_aries, key_taurus)
        self.keyboard.add(key_gemini, key_cancer)
        self.keyboard.add(key_leo, key_virgo)
        self.keyboard.add(key_libra, key_scorpio)
        self.keyboard.add(key_sagittarius, key_capricorn)
        self.keyboard.add(key_aquarius, key_pisces)

        return self.keyboard

    def get_default_keyboard(self, chat_type):
        return self.start_keyboard() if chat_type == PRIVATE_CHAT else None

    def __clear_keyborad(self):
        self.keyboard.keyboard.clear()


def greeting() -> str:
    """Generator of greetings for /start and /help commands"""
    options = [
        "Aight, mate!\nWhat can I do for you??",
        "Ahoy, matey!\nWant a cup of coffee or a secret mission?",
        "This call may be recorded for training purposes.\nProceed, please.",
        "How does a lion greet the other animals in the field?\n- Pleased to eat you.",
        "Ghostbusters, whatya want?",
        "What's cookin', good lookin'?",
        "Hey there, freshman!\nWhat's good?",
        "Welcome to the club, boss!\nWhat's the plan?"
        "I came here to speak English and\nmeet my friend.\nAs you can see, I have spoken.",
        "Shhh, speak quiet,\nthey are watching us.\nWere you followed?",
        "Salutations are greetings!\nNeed something?",
        "Alright alright alright!",
        "Bot. James Bot.\nAnd you?",
        "You know what they say in China?\n They say: Ciao!"
    ]
    commands = "\n\n/gpt (your question here) to send a question to ChatGPT\n" \
               "/urban (word or phrase) to look up a definition in Urban Dictionary\n"

    return choice(options) + commands


class CallBackData(str, Enum):
    """Enum that contains all types of callback data"""
    HELLO = auto()
    URBAN = auto()
    HOROSCOPE = auto()
    ZODIAC = auto()
    GPT = auto()


class WhackyBotValidationException(Exception):
    """Custom validation exception for Whacky bot"""
    pass
