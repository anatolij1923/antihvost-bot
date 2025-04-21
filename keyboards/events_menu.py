from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_events_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Добавить мероприятие", callback_data="event:add"),
        InlineKeyboardButton(text="Просмотр мероприятий", callback_data="event:list")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_event_actions_kb(event_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Удалить", callback_data=f"event:delete:{event_id}"),
        InlineKeyboardButton(text="Назад", callback_data="event:back")
    )
    builder.adjust(1)
    return builder.as_markup()