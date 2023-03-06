import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Optional

from app.utils import WhackyBotValidationException

BOT_TOKEN_ENV: Final[str] = "BOT_TOKEN"
OPENAI_TOKEN_ENV: Final[str] = "OPENAI_TOKEN"
BOT_TOKEN_CONSTANT: Final[str] = ""
OPENAI_TOKEN_CONSTANT: Final[str] = ""

SERVICE_ERROR_MSG: Final[str] = "Something went wrong with the request to the service. Please contact the admin."

WELCOME_STICKER: Final[str] = "CAACAgUAAxkBAAEBjDZfpW1LILCOSNQx69Q8e29SyuntEAACHAcAAszG4gLu8__0XRJBEx4E"
MEDIA_DIR: Path = Path(__file__).parent / "media"
GREETING_VOICE: Path = MEDIA_DIR / "greeting.ogg"


@dataclass
class BotConfig:
    """Class to collect all app's configuration and check the required tokens set up"""

    BOT_TOKEN: Optional[str] = os.getenv(BOT_TOKEN_ENV) or BOT_TOKEN_CONSTANT
    OPENAI_TOKEN: Optional[str] = os.getenv(OPENAI_TOKEN_ENV) or OPENAI_TOKEN_CONSTANT
    LOG_LEVEL = logging.INFO
    CALLBACK_CACHE_DELAY: float = 0.6

    def __post__init__(self):
        if not self.BOT_TOKEN or not self.OPENAI_TOKEN:
            raise WhackyBotValidationException(
                "Please set up tokens for TeleBot and OpenAI"
            )


cfg = BotConfig()
