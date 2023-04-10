import logging
import os
from dataclasses import dataclass

from pathlib import Path
from typing import Final, Optional, Dict, ClassVar
from dotenv import load_dotenv

from telebot import TeleBot

from app.utils import WhackyBotValidationException

# environment variables imported from file
current_dir = Path(__file__).parent.parent
dotenv_path = current_dir / ".env"

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


ENV: Final[str] = "ENV"
DEV: Final[str] = "DEV"
TEST: Final[str] = "TEST"
PROD: Final[str] = "PROD"
BOT_TOKEN_ENV: Final[str] = "BOT_TOKEN"
OPENAI_TOKEN_ENV: Final[str] = "OPENAI_TOKEN"

SERVICE_ERROR_MSG: Final[
    str
] = "Something went wrong with the request to the service. Please contact the admin."

WELCOME_STICKER: Final[
    str
] = "CAACAgUAAxkBAAEBjDZfpW1LILCOSNQx69Q8e29SyuntEAACHAcAAszG4gLu8__0XRJBEx4E"
MEDIA_DIR: Path = Path(__file__).parent / "media"
GREETING_VOICE: Path = MEDIA_DIR / "greeting.ogg"


@dataclass
class BotConfig:
    """Class to collect all app's configuration and check the required tokens set up"""

    BOT_TOKEN: Optional[str] = None
    OPENAI_TOKEN: Optional[str] = None
    LOG_LEVEL = logging.INFO
    CALLBACK_CACHE_DELAY: float = 0.6
    _bot_type: ClassVar = TeleBot
    _config: ClassVar = None

    def __post_init__(self):
        if not self.bot_token or not self.openai_token():
            raise WhackyBotValidationException("Please set up tokens for services")

    @classmethod
    def get_config(cls) -> "BotConfig":
        """Factory method to maintain a singleton BotConfig instance"""
        if not cls._config:
            env = os.getenv(ENV)
            config = CONFIGS.get(env, DevBotConfig)
            cls._config = config()

        return cls._config

    @property
    def bot_token(self):
        """Getter for Telegram bot token to allow lazy initialization"""
        if not self.OPENAI_TOKEN:
            self.OPENAI_TOKEN = os.getenv(OPENAI_TOKEN_ENV)
        return self.OPENAI_TOKEN

    def openai_token(self):
        """Getter for OpenAI token to allow lazy initialization"""
        if not self.BOT_TOKEN:
            self.BOT_TOKEN = os.getenv(BOT_TOKEN_ENV)
        return self.BOT_TOKEN


@dataclass
class DevBotConfig(BotConfig):
    """DEV instance of BotConfig"""

    LOG_LEVEL = logging.DEBUG


@dataclass
class TestBotConfig(BotConfig):
    """TEST instance of BotConfig"""

    BOT_TOKEN: Optional[str] = "Test"
    OPENAI_TOKEN: Optional[str] = "Test"
    TESTING: bool = True


@dataclass
class ProdBotConfig(BotConfig):
    """PROD instance of BotConfig"""

    pass


CONFIGS: Dict = {
    DEV: DevBotConfig,
    TEST: TestBotConfig,
    PROD: ProdBotConfig,
}
