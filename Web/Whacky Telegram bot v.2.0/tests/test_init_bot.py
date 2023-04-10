import pytest

from app import init_bot_factory, WhackyTeleBot
from app.config import BotConfig, TestBotConfig, ProdBotConfig
from tests.fakes import FakeBot


def test_init_bot_factory_default():
    cfg = BotConfig.get_config()
    bot = init_bot_factory(cfg)

    assert isinstance(bot, WhackyTeleBot)
    assert isinstance(bot.bot, cfg._bot_type)


def test_init_bot_factory_not_implemented_error():
    class UnsupportedBot:
        pass

    cfg = BotConfig.get_config()
    cfg._bot_type = UnsupportedBot
    with pytest.raises(NotImplementedError):
        init_bot_factory(cfg)


def test_init_bot_factory_test():
    cfg = TestBotConfig()
    bot = init_bot_factory(cfg)

    assert isinstance(bot, WhackyTeleBot)
    assert isinstance(bot.bot, FakeBot)


def test_init_bot_factory_prod():
    cfg = ProdBotConfig()
    bot = init_bot_factory(cfg)

    assert isinstance(bot, WhackyTeleBot)
    assert isinstance(bot.bot, cfg._bot_type)
