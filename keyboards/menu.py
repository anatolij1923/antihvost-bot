from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="📝 Создать задание", callback_data="create_task"),
            InlineKeyboardButton(text="📋 Мои задания", callback_data="my_tasks"),
        ],
        [
            InlineKeyboardButton(text="📆 Календарь", callback_data="calendar"),
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_settings_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
            InlineKeyboardButton(text="🔔 Уведомления", callback_data="notifications"),
        ],
        [
            InlineKeyboardButton(text="👤 Поддержка", callback_data="support"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 