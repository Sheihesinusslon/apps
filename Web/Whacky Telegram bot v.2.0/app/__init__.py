from typing import cast

import telebot

from app.config import BotConfig, ProdBotConfig, TestBotConfig
from app.interfaces import IKeyboardManager, ITeleBot, IWhackyBot
from app.utils import KeyboardManager
from app.services import UrbanDict, GPT, WhackyTeleBot
from tests.fakes import (
    FakeBot,
    FakeKeyboard,
    FakeUrbanClient,
    FakeOpenaiClient,
    FakeButton,
)


def init_bot_dev(cfg: BotConfig) -> IWhackyBot:
    """Initializes a DEV bot instance"""
    if issubclass(cfg._bot_type, telebot.TeleBot):
        bot = cast(
            ITeleBot,
            telebot.TeleBot(cfg.BOT_TOKEN, colorful_logs=True, parse_mode="markdown"),
        )
        keyboard = cast(
            IKeyboardManager,
            KeyboardManager(
                keyboard=telebot.types.InlineKeyboardMarkup(),
                button=telebot.types.InlineKeyboardButton,
            ),
        )

        return cast(
            IWhackyBot,
            WhackyTeleBot(bot=bot, keyboard_manager=keyboard),
        )
    raise NotImplementedError("Unsupported bot type")


def init_bot_prod(cfg: BotConfig) -> IWhackyBot:
    """Initializes a PROD bot instance"""
    return init_bot_dev(cfg)


def init_bot_test(_cfg: BotConfig) -> IWhackyBot:
    """Initializes a TEST bot instance with Fakes instead of real clients"""
    bot = cast(ITeleBot, FakeBot())
    keyboard = FakeKeyboard()
    km = KeyboardManager(keyboard=keyboard, button=FakeButton)
    urban_dict = UrbanDict(FakeUrbanClient())
    gpt = GPT(openai_client=FakeOpenaiClient())
    return cast(
        IWhackyBot,
        WhackyTeleBot(bot=bot, keyboard_manager=km, urban_dict=urban_dict, gpt=gpt),
    )


def init_bot_factory(cfg: BotConfig) -> IWhackyBot:
    """Factory function to call necessary init bot function based on the config instance
    and return a respective bot instance"""
    if isinstance(cfg, ProdBotConfig):
        return init_bot_prod(cfg)
    if isinstance(cfg, TestBotConfig):
        return init_bot_test(cfg)
    return init_bot_dev(cfg)
