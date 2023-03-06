import logging

from app.config import cfg

logger = logging.getLogger("TeleBot")
logger.setLevel(cfg.LOG_LEVEL)
