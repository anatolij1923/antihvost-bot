from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import uuid

from states.lab_states import AssignmentStates
from keyboards.lab_menu import (
    get_assignment_type_kb,
    get_assignments_menu_kb,
    get_assignment_actions_kb,
    get_status_choice_kb,
    get_assignment_list_kb,
    get_subject_choice_kb,
    get_subject_name
)
from utils.models import Assignment, AssignmentStatus
from database.db import add_assignment, get_user_assignments, update_assignment_status, delete_assignment

router = Router()

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
    
    if assignment_type == "lab":
        await callback.message.edit_text(
            "Выберите предмет:",
            reply_markup=get_subject_choice_kb()
        )
        await state.set_state(AssignmentStates.choosing_subject)
    else:
        await callback.message.edit_text(
            "Введите название задания:",
            reply_markup=None
        )
        await state.set_state(AssignmentStates.entering_name)

@router.callback_query(StateFilter(AssignmentStates.choosing_subject))
async def process_subject_choice(callback: CallbackQuery, state: FSMContext):
    subject = callback.data.split(":")[1]
    await state.update_data(subject=subject)
    
    await callback.message.edit_text(
        "Введите название лабораторной работы:",
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
        
        # Добавляем задание в базу данных
        add_assignment(
            user_id=message.from_user.id,
            title=data["name"],
            description=data["description"],
            due_date=deadline,
            assignment_type=data["type"],
            subject=data.get("subject")
        )
        
        subject_text = f"Предмет: {data['subject'].replace('_', ' ').title()}\n" if data.get("subject") else ""
        
        await message.answer(
            f"Задание успешно добавлено!\n\n"
            f"Тип: {'Лабораторная работа' if data['type'] == 'lab' else 'Домашнее задание'}\n"
            f"{subject_text}"
            f"Название: {data['name']}\n"
            f"Дедлайн: {deadline.strftime('%d.%m.%Y %H:%M')}",
            reply_markup=get_assignments_menu_kb()
        )
        await state.clear()
        
    except ValueError:
        await message.answer(
            "Неверный формат даты. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Например: 31.12.2024 23:59"
        )

@router.callback_query(F.data.startswith("assignment:view:"))
async def view_assignment(callback: CallbackQuery):
    assignment_id = int(callback.data.split(":")[2])
    assignments = get_user_assignments(callback.from_user.id)
    assignment = next((a for a in assignments if a[0] == assignment_id), None)
    
    if not assignment:
        await callback.answer("Задание не найдено!")
        return
    
    try:
        status = AssignmentStatus(assignment[5])
    except ValueError:
        status = AssignmentStatus.NOT_STARTED
        
    status_emoji = {
        AssignmentStatus.NOT_STARTED: "⏳",
        AssignmentStatus.IN_PROGRESS: "🔄",
        AssignmentStatus.COMPLETED: "✅",
        AssignmentStatus.SUBMITTED: "📤"
    }[status]
    
    subject_text = f"Предмет: {get_subject_name(assignment[7])}\n" if assignment[7] else ""
    
    text = (
        f"{'🔬 Лаба' if assignment[6] == 'lab' else '📚 ДЗ'}: {assignment[2]}\n"
        f"{subject_text}"
        f"Описание: {assignment[3]}\n"
        f"Дедлайн: {datetime.strptime(assignment[4], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')}\n"
        f"Статус: {status_emoji} {get_status_text(status)}\n\n"
        f"Выберите действие:"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_assignment_actions_kb(assignment_id)
    )

@router.callback_query(F.data.startswith("assignment:change_status:"))
async def change_assignment_status(callback: CallbackQuery):
    assignment_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "Выберите новый статус:",
        reply_markup=get_status_choice_kb(assignment_id)
    )

@router.callback_query(F.data.startswith("status:"))
async def process_status_change(callback: CallbackQuery):
    status, assignment_id = callback.data.split(":")[1:]
    assignment_id = int(assignment_id)
    
    # Обновляем статус в базе данных
    update_assignment_status(assignment_id, callback.from_user.id, status)
    
    await callback.message.edit_text(
        "Статус успешно обновлен!",
        reply_markup=get_assignments_menu_kb()
    )

@router.callback_query(F.data.startswith("assignment:delete:"))
async def delete_assignment_handler(callback: CallbackQuery):
    assignment_id = int(callback.data.split(":")[2])
    
    # Удаляем задание из базы данных
    delete_assignment(assignment_id, callback.from_user.id)
    
    await callback.message.edit_text(
        "Задание успешно удалено!",
        reply_markup=get_assignments_menu_kb()
    )

@router.callback_query(F.data == "assignment:deadlines")
async def show_deadlines(callback: CallbackQuery):
    now = datetime.now()
    assignments = get_user_assignments(callback.from_user.id)
    active_assignments = [a for a in assignments if datetime.strptime(a[4], '%Y-%m-%d %H:%M:%S') > now]
    
    if not active_assignments:
        await callback.message.edit_text(
            "У вас нет активных дедлайнов!",
            reply_markup=get_assignments_menu_kb()
        )
        return

    text = "Ваши активные дедлайны:\n\n"
    for assignment in sorted(active_assignments, key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')):
        time_left = datetime.strptime(assignment[4], '%Y-%m-%d %H:%M:%S') - now
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        try:
            status = AssignmentStatus(assignment[5])
        except ValueError:
            status = AssignmentStatus.NOT_STARTED
            
        status_emoji = {
            AssignmentStatus.NOT_STARTED: "⏳",
            AssignmentStatus.IN_PROGRESS: "🔄",
            AssignmentStatus.COMPLETED: "✅",
            AssignmentStatus.SUBMITTED: "📤"
        }[status]
        
        subject_text = f"Предмет: {get_subject_name(assignment[7])}\n" if assignment[7] else ""
        
        text += (
            f"{'🔬 Лаба' if assignment[6] == 'lab' else '📚 ДЗ'}: {assignment[2]}\n"
            f"{subject_text}"
            f"Описание: {assignment[3]}\n"
            f"Дедлайн: {datetime.strptime(assignment[4], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')}\n"
            f"Статус: {status_emoji} {get_status_text(status)}\n"
            f"Осталось: {days_left}д {hours_left}ч\n\n"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_assignments_menu_kb()
    )

@router.callback_query(F.data == "assignment:list")
async def show_assignments_list(callback: CallbackQuery):
    assignments = get_user_assignments(callback.from_user.id)
    if not assignments:
        await callback.message.edit_text(
            "У вас пока нет добавленных заданий!",
            reply_markup=get_assignments_menu_kb()
        )
        return

    builder = InlineKeyboardBuilder()
    for assignment in sorted(assignments, key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')):
        try:
            status = AssignmentStatus(assignment[5])
        except ValueError:
            status = AssignmentStatus.NOT_STARTED
            
        status_emoji = {
            AssignmentStatus.NOT_STARTED: "⏳",
            AssignmentStatus.IN_PROGRESS: "🔄",
            AssignmentStatus.COMPLETED: "✅",
            AssignmentStatus.SUBMITTED: "📤"
        }[status]
        
        builder.add(
            InlineKeyboardButton(
                text=f"{'🔬' if assignment[6] == 'lab' else '📚'} {assignment[2]} - {status_emoji} {get_status_text(status)}",
                callback_data=f"assignment:view:{assignment[0]}"
            )
        )
    
    builder.add(InlineKeyboardButton(text="Назад", callback_data="menu:back"))
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Выберите задание для просмотра и изменения статуса:",
        reply_markup=builder.as_markup()
    ) 