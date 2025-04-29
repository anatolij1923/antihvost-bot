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
    get_assignment_actions_kb,
    get_status_choice_kb,
    get_assignment_list_kb
)
from utils.models import Assignment, AssignmentStatus

router = Router()

# Временное хранилище заданий (в реальном проекте лучше использовать базу данных)
assignments = {}

def get_status_text(status: AssignmentStatus) -> str:
    status_texts = {
        AssignmentStatus.NOT_STARTED: "Не начато",
        AssignmentStatus.IN_PROGRESS: "В работе",
        AssignmentStatus.COMPLETED: "Готово",
        AssignmentStatus.SUBMITTED: "Сдано"
    }
    return status_texts[status]

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

@router.callback_query(F.data.startswith("assignment:change_status:"))
async def change_assignment_status(callback: CallbackQuery):
    assignment_id = callback.data.split(":")[2]
    assignment = assignments.get(assignment_id)
    
    if not assignment:
        await callback.answer("Задание не найдено!")
        return
    
    await callback.message.edit_text(
        f"Выберите новый статус для задания '{assignment.name}':",
        reply_markup=get_status_choice_kb(assignment_id)
    )

@router.callback_query(F.data.startswith("status:"))
async def process_status_change(callback: CallbackQuery):
    status, assignment_id = callback.data.split(":")[1], callback.data.split(":")[2]
    assignment = assignments.get(assignment_id)
    
    if not assignment:
        await callback.answer("Задание не найдено!")
        return
    
    assignment.status = AssignmentStatus(status)
    
    status_emoji = {
        AssignmentStatus.NOT_STARTED: "⏳",
        AssignmentStatus.IN_PROGRESS: "🔄",
        AssignmentStatus.COMPLETED: "✅",
        AssignmentStatus.SUBMITTED: "📤"
    }[assignment.status]
    
    await callback.message.edit_text(
        f"Статус задания '{assignment.name}' изменен на {status_emoji} {get_status_text(assignment.status)}",
        reply_markup=get_assignment_actions_kb(assignment_id)
    )

@router.callback_query(F.data.startswith("assignment:view:"))
async def view_assignment(callback: CallbackQuery):
    assignment_id = callback.data.split(":")[2]
    assignment = assignments.get(assignment_id)
    
    if not assignment:
        await callback.answer("Задание не найдено!")
        return
    
    status_emoji = {
        AssignmentStatus.NOT_STARTED: "⏳",
        AssignmentStatus.IN_PROGRESS: "🔄",
        AssignmentStatus.COMPLETED: "✅",
        AssignmentStatus.SUBMITTED: "📤"
    }[assignment.status]
    
    text = (
        f"{'🔬 Лаба' if assignment.type == 'lab' else '📚 ДЗ'}: {assignment.name}\n"
        f"Дедлайн: {assignment.deadline.strftime('%d.%m.%Y %H:%M')}\n"
        f"Статус: {status_emoji} {get_status_text(assignment.status)}\n"
        f"Описание: {assignment.description}\n\n"
        f"Выберите действие:"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_assignment_actions_kb(assignment_id)
    )

@router.callback_query(F.data == "assignment:list")
async def list_assignments(callback: CallbackQuery):
    user_assignments = {k: v for k, v in assignments.items() if v.created_by == callback.from_user.id}
    
    if not user_assignments:
        await callback.message.edit_text(
            "У вас пока нет добавленных заданий!",
            reply_markup=get_assignments_menu_kb()
        )
        return

    text = "Выберите задание для просмотра:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_assignment_list_kb(user_assignments)
    )

@router.callback_query(F.data == "assignment:deadlines")
async def show_deadlines(callback: CallbackQuery):
    now = datetime.now()
    active_assignments = {
        k: v for k, v in assignments.items()
        if v.deadline > now and v.created_by == callback.from_user.id
    }
    
    if not active_assignments:
        await callback.message.edit_text(
            "У вас нет активных дедлайнов!",
            reply_markup=get_assignments_menu_kb()
        )
        return

    text = "Ваши активные дедлайны:\n\n"
    for assignment in sorted(active_assignments.values(), key=lambda x: x.deadline):
        time_left = assignment.deadline - now
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        status_emoji = {
            AssignmentStatus.NOT_STARTED: "⏳",
            AssignmentStatus.IN_PROGRESS: "🔄",
            AssignmentStatus.COMPLETED: "✅",
            AssignmentStatus.SUBMITTED: "📤"
        }[assignment.status]
        
        text += (
            f"{'🔬 Лаба' if assignment.type == 'lab' else '📚 ДЗ'}: {assignment.name}\n"
            f"Дедлайн: {assignment.deadline.strftime('%d.%m.%Y %H:%M')}\n"
            f"Статус: {status_emoji} {get_status_text(assignment.status)}\n"
            f"Осталось: {days_left}д {hours_left}ч\n\n"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_assignments_menu_kb()
    ) 