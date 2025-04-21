from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

events_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить мероприятие")],
        [KeyboardButton(text="Просмотр мероприятий")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)