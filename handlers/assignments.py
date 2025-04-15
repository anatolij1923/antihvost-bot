from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime
import uuid

from states.lab_states import AssignmentStates
from keyboards.lab_menu import (
    get_assignment_type_kb,
    get_assignments_menu_kb,
    get_assignment_actions_kb
)
from utils.models import Assignment

router = Router()

# Временное хранилище заданий (в реальном проекте лучше использовать базу данных)
assignments = {}

@router.message(Command("assignments"))
async def show_assignments_menu(message: Message):
    await message.answer(
        "Меню управления заданиями:",
        reply_markup=get_assignments_menu_kb()
    )

@router.callback_query(F.data == "assignment:add")
async def start_assignment_adding(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Выберите тип задания:",
        reply_markup=get_assignment_type_kb()
    )
    await state.set_state(AssignmentStates.choosing_type)

@router.callback_query(StateFilter(AssignmentStates.choosing_type))
async def process_assignment_type(callback: CallbackQuery, state: FSMContext):
    assignment_type = callback.data.split(":")[1]
    await state.update_data(type=assignment_type)
    
    await callback.message.edit_text(
        "Введите название задания:",
        reply_markup=None
    )
    await state.set_state(AssignmentStates.entering_name)

@router.message(StateFilter(AssignmentStates.entering_name))
async def process_assignment_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание задания:")
    await state.set_state(AssignmentStates.entering_description)

@router.message(StateFilter(AssignmentStates.entering_description))
async def process_assignment_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        "Введите дедлайн в формате ДД.ММ.ГГГГ ЧЧ:ММ\n"
        "Например: 31.12.2024 23:59"
    )
    await state.set_state(AssignmentStates.entering_deadline)

@router.message(StateFilter(AssignmentStates.entering_deadline))
async def process_assignment_deadline(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        data = await state.get_data()
        
        assignment = Assignment(
            id=str(uuid.uuid4()),
            type=data["type"],
            name=data["name"],
            description=data["description"],
            deadline=deadline,
            created_at=datetime.now(),
            created_by=message.from_user.id
        )
        
        assignments[assignment.id] = assignment
        
        await message.answer(
            f"Задание успешно добавлено!\n\n"
            f"Тип: {'Лабораторная работа' if assignment.type == 'lab' else 'Домашнее задание'}\n"
            f"Название: {assignment.name}\n"
            f"Дедлайн: {assignment.deadline.strftime('%d.%m.%Y %H:%M')}",
            reply_markup=get_assignments_menu_kb()
        )
        await state.clear()
        
    except ValueError:
        await message.answer(
            "Неверный формат даты. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Например: 31.12.2024 23:59"
        )

@router.callback_query(F.data == "assignment:list")
async def list_assignments(callback: CallbackQuery):
    if not assignments:
        await callback.message.edit_text(
            "Список заданий пуст!",
            reply_markup=get_assignments_menu_kb()
        )
        return

    text = "Список всех заданий:\n\n"
    for assignment in assignments.values():
        text += (
            f"{'🔬 Лаба' if assignment.type == 'lab' else '📚 ДЗ'}: {assignment.name}\n"
            f"Дедлайн: {assignment.deadline.strftime('%d.%m.%Y %H:%M')}\n"
            f"Описание: {assignment.description}\n\n"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_assignments_menu_kb()
    )

@router.callback_query(F.data == "assignment:deadlines")
async def show_deadlines(callback: CallbackQuery):
    now = datetime.now()
    active_assignments = {
        k: v for k, v in assignments.items()
        if v.deadline > now
    }
    
    if not active_assignments:
        await callback.message.edit_text(
            "Нет активных дедлайнов!",
            reply_markup=get_assignments_menu_kb()
        )
        return

    text = "Активные дедлайны:\n\n"
    for assignment in sorted(active_assignments.values(), key=lambda x: x.deadline):
        time_left = assignment.deadline - now
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        text += (
            f"{'🔬 Лаба' if assignment.type == 'lab' else '📚 ДЗ'}: {assignment.name}\n"
            f"Дедлайн: {assignment.deadline.strftime('%d.%m.%Y %H:%M')}\n"
            f"Осталось: {days_left}д {hours_left}ч\n\n"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_assignments_menu_kb()
    ) 