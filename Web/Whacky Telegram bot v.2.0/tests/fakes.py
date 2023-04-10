import random
from dataclasses import dataclass, field
from typing import List

from app.utils import PRIVATE_CHAT, CallBackData


@dataclass
class FakeChat:
    id: int = 1
    type: str = PRIVATE_CHAT


@dataclass
class FakeMessage:
    chat: FakeChat = FakeChat()
    text: str = "Some Message"


@dataclass
class FakeUser:
    id: int = 1


@dataclass
class FakeCall:
    data: CallBackData
    message: FakeMessage = FakeMessage()
    from_user: FakeUser = FakeUser()


class FakeBot:
    def __init__(self):
        self.running = False
        self.message_sent = False
        self.sticker_sent = False
        self.voice_sent = False

    def message_handler(func, *a, **kw):
        def inner(*args, **kwargs):
            func(*args, **kwargs)

        return inner

    @staticmethod
    def callback_query_handler(func, *a, **kw):
        def inner(*args, **kwargs):
            func(*args, **kwargs)

        return inner

    def send_message(self, message, *args, **kwargs):
        self.message_sent = True
        return message

    def send_sticker(self, *args, **kwargs):
        self.sticker_sent = True

    def send_voice(self, *args, **kwargs):
        self.voice_sent = True

    def polling(self, *args, **kwargs):
        self.running = True

    def reset(self):
        self.running = False
        self.message_sent = False
        self.sticker_sent = False
        self.voice_sent = False

    def __call__(self, *args, **kwargs):
        return self


@dataclass
class FakeButton:
    text: str
    callback_data: str


class FakeKeyboard:
    def __init__(self, keyboard=None):
        self.keyboard: List[List[FakeButton]] = keyboard or []

    def add(self, *args, **kwargs):
        button_array = [button for button in args]
        self.keyboard.append(button_array)

    def clear(self):
        self.keyboard.clear()

    def reset(self):
        self.clear()


@dataclass
class FakeUrbanDefinition:
    word: str
    definition: str


class FakeUrbanClient:
    def __init__(self):
        self.called = False
        self.definitions: List[FakeUrbanDefinition] = [
            FakeUrbanDefinition("word_1", "definition_1"),
            FakeUrbanDefinition("word_2", "definition_2"),
            FakeUrbanDefinition("word_3", "definition_3"),
            FakeUrbanDefinition("word_4", "definition_4"),
            FakeUrbanDefinition("word_5", "definition_5"),
            FakeUrbanDefinition("word_6", "definition_6"),
        ]

    def get_definition(self, prompt):
        for definition in self.definitions:
            definition.word = prompt
        self.called = True
        return self.definitions

    def get_random_definition(self):
        self.called = True
        return random.choices(self.definitions, k=5)

    def reset(self):
        self.called = False


@dataclass
class FakeResponse:
    text: str = "Response"


@dataclass
class FakeCompletion:
    choices: List[FakeResponse] = field(default_factory=list)

    def __post_init__(self):
        self.choices.append(FakeResponse())


class FakeOpenaiClient:
    def __init__(self):
        self.called = False

    def create(self, *a, **kw):
        self.called = True
        return FakeCompletion()

    def acreate(self, *a, **kw):
        ...

    def reset(self):
        self.called = False
