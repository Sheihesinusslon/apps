from typing import List

import pytest

from app.services.horoscope import get_horoscope
from app.utils import greeting, KeyboardManager, PRIVATE_CHAT
from tests.fakes import FakeKeyboard, FakeButton

NUM_HOROSCOPE_SIGNS = 12


@pytest.fixture
def test_km(monkeypatch):
    with monkeypatch.context():
        keyboard = FakeKeyboard()
        km = KeyboardManager(keyboard=keyboard, button=FakeButton)
        yield km
        keyboard.reset()


def test_greeting():
    response = greeting()

    assert isinstance(response, str)


def test_horoscope():
    response = get_horoscope()

    assert isinstance(response, str)


class TestKeyboardManager:
    def test_start_keyboard(self, test_km):
        keyboard = test_km.start_keyboard()

        assert isinstance(keyboard.keyboard, List)

    def test_horoscope_keyboard(self, test_km):
        keyboard = test_km.horoscope_keyboard()

        buttons = [button for row in keyboard.keyboard for button in row]
        assert len(buttons) == NUM_HOROSCOPE_SIGNS

    def test_get_default_keyboard(self, test_km):
        keyboard1 = test_km.get_default_keyboard("group")

        assert keyboard1 is None

        keyboard2 = test_km.get_default_keyboard(PRIVATE_CHAT)
        assert isinstance(keyboard2.keyboard, List)
