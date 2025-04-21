from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# кнопка отмены
cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)
# главное меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Просмотр лабораторных")],
        [KeyboardButton(text="📖 Домашние задания")],
        [KeyboardButton(text="🏆 Рейтинг")],
        [KeyboardButton(text="🛠 Управление лабораторными")],
        [KeyboardButton(text="📅 Мероприятия")],
        [KeyboardButton(text="Не нажимать❗❗❗")]
    ],
    resize_keyboard=True
)
