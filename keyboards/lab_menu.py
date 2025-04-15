from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_assignment_type_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лабораторная работа", callback_data="assignment_type:lab"),
        InlineKeyboardButton(text="Домашнее задание", callback_data="assignment_type:homework")
    )
    return builder.as_markup()

def get_assignments_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Добавить задание", callback_data="assignment:add"),
        InlineKeyboardButton(text="Список заданий", callback_data="assignment:list"),
        InlineKeyboardButton(text="Активные дедлайны", callback_data="assignment:deadlines")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_assignment_actions_kb(assignment_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Изменить дедлайн", callback_data=f"assignment:edit_deadline:{assignment_id}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"assignment:delete:{assignment_id}"),
        InlineKeyboardButton(text="Назад", callback_data="assignment:back")
    )
    builder.adjust(1)
    return builder.as_markup()
