from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру основных настроек"""
    keyboard = [
        [
            InlineKeyboardButton(text="🔔 Уведомления", callback_data="notifications"),
        ],
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        ],
        [
            InlineKeyboardButton(text="❓ Поддержка", callback_data="support"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_notifications_keyboard(is_enabled: bool) -> InlineKeyboardMarkup:
    """Создает клавиатуру настроек уведомлений"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Включить" if not is_enabled else "❌ Выключить",
                callback_data="toggle_notifications"
            ),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_settings"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 