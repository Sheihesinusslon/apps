import pytest

from app import (
    TestBotConfig,
    IWhackyBot,
    init_bot_factory,
    WhackyTeleBot,
    UrbanDict,
    GPT,
)
from run import run_bot
from tests.fakes import FakeMessage, FakeCall, FakeBot, FakeKeyboard, FakeButton
from app.utils import CallBackData, KeyboardManager


@pytest.fixture
def test_whacky_bot(monkeypatch):
    with monkeypatch.context():
        cfg = TestBotConfig()
        whacky_bot: IWhackyBot = init_bot_factory(cfg)
        run_bot(whacky_bot.bot, whacky_bot)

        assert whacky_bot.bot.running
        yield whacky_bot
        whacky_bot.bot.reset()


class TestWhackyBot:
    def test_welcome(self, test_whacky_bot):
        test_whacky_bot.welcome(FakeMessage())

        assert test_whacky_bot.bot.sticker_sent
        assert test_whacky_bot.bot.message_sent

    def test_handle_text_messages(self, test_whacky_bot):
        test_whacky_bot.handle_text_messages(FakeMessage())

        assert test_whacky_bot.bot.message_sent
        assert test_whacky_bot.gpt.openai_client.called

    def test_handle_ud_request(self, test_whacky_bot):
        test_whacky_bot.handle_ud_request(FakeMessage())

        assert test_whacky_bot.bot.message_sent
        assert test_whacky_bot.urban_dict.client.called

    def test_handle_gpt_request(self, test_whacky_bot):
        test_whacky_bot.handle_gpt_request(FakeMessage())

        assert test_whacky_bot.bot.message_sent
        assert test_whacky_bot.gpt.openai_client.called

    def test_handle_gpt_request_empty_prompt(self, test_whacky_bot):
        test_whacky_bot.handle_gpt_request(FakeMessage(text=""))

        assert test_whacky_bot.bot.message_sent
        assert not test_whacky_bot.gpt.openai_client.called

    @pytest.mark.parametrize(
        "data", (CallBackData.URBAN, CallBackData.HOROSCOPE, CallBackData.GPT)
    )
    def test_handle_keyboard_messages(self, data, test_whacky_bot):
        test_whacky_bot.handle_keyboard_messages(FakeCall(data=data))

        assert test_whacky_bot.bot.message_sent

    def test_handle_keyboard_messages_horoscope(self, test_whacky_bot):
        test_whacky_bot.handle_keyboard_messages(FakeCall(data=CallBackData.ZODIAC))

        assert test_whacky_bot.bot.message_sent
        assert test_whacky_bot.gpt.openai_client.called

    def test_handle_keyboard_messages_hello(self, test_whacky_bot):
        test_whacky_bot.handle_keyboard_messages(FakeCall(data=CallBackData.HELLO))

        assert test_whacky_bot.bot.sticker_sent
        assert test_whacky_bot.bot.voice_sent

    def test_properties_lazy_init(self):
        bot = FakeBot()
        keyboard = FakeKeyboard()
        km = KeyboardManager(keyboard=keyboard, button=FakeButton)
        whacky_bot = WhackyTeleBot(bot=bot, keyboard_manager=km)

        assert whacky_bot.urban_dict
        assert isinstance(whacky_bot.urban_dict, UrbanDict)
        assert whacky_bot.gpt
        assert isinstance(whacky_bot.gpt, GPT)
