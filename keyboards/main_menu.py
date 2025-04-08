from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)
