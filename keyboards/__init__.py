from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Задания")],
            [KeyboardButton(text="Мероприятия")],
            [KeyboardButton(text="Профиль")]
        ],
        resize_keyboard=True
    )
    return keyboard

__all__ = ['get_main_menu'] 