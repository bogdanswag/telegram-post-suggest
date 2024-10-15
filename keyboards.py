from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def suggest_post() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Предложить пост")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
