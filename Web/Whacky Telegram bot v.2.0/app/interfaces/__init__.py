from app.interfaces.bots import ITeleBot
from app.interfaces.keyboards import ITeleKeyboard, ITeleButton
from app.interfaces.keyboard_manager import IKeyboardManager
from app.interfaces.whacky_bot_adapter import IWhackyBot
from app.interfaces.urban_dict import IUrbanClient
from app.interfaces.gpt import IGPT

__all__ = [
    "ITeleBot",
    "ITeleKeyboard",
    "ITeleButton",
    "IKeyboardManager",
    "IWhackyBot",
    "IUrbanClient",
    "IGPT",
]
