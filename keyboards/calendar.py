from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_calendar_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="📆 Сегодня", callback_data="calendar_today"),
        ],
        [
            InlineKeyboardButton(text="📆 На этой неделе", callback_data="calendar_week"),
        ],
        [
            InlineKeyboardButton(text="📆 Весь месяц", callback_data="calendar_month"),
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 