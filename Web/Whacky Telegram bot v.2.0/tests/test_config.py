import pytest

from app.config import BotConfig, DevBotConfig, TestBotConfig, ENV, TEST, BOT_TOKEN_ENV
from app.utils import WhackyBotValidationException


def test_bot_config_default():
    config = BotConfig.get_config()

    assert isinstance(config, DevBotConfig)
    assert config.BOT_TOKEN
    assert config.OPENAI_TOKEN


def test_bot_config_singleton():
    config1 = BotConfig.get_config()
    config2 = BotConfig.get_config()

    assert config1 is config2


@pytest.mark.skip
def test_bot_config_test(monkeypatch):
    monkeypatch.setenv(ENV, TEST)
    config = BotConfig.get_config()

    assert isinstance(config, TestBotConfig)
    assert config.BOT_TOKEN == "Test"
    assert config.TESTING is True


@pytest.mark.skip
def test_bot_config_raises_error(monkeypatch):
    monkeypatch.setenv(BOT_TOKEN_ENV, "")
    with pytest.raises(WhackyBotValidationException):
        BotConfig.get_config()
