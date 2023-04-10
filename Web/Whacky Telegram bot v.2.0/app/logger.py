import logging

from app.config import BotConfig

cfg: BotConfig = BotConfig.get_config()
logger = logging.getLogger("TeleBot")
logger.setLevel(cfg.LOG_LEVEL)
