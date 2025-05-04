from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = [
        [
            KeyboardButton(text="📝 Создать задание"),
            KeyboardButton(text="📋 Мои задания"),
        ],
        [
            KeyboardButton(text="📆 Календарь"),
            KeyboardButton(text="⚙️ Настройки"),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True) 