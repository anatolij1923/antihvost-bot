from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import main_menu_keyboard
from keyboards.lab_menu import get_assignments_menu_kb, get_status_text, get_subject_name
from keyboards.events_menu import get_events_menu_kb
from database.db import get_user_fullname, get_user_assignments
from datetime import datetime
from utils.models import AssignmentStatus

router = Router()

@router.message(F.text == "📚 Просмотр лабораторных")
async def handle_labs_view(message: Message):
    assignments = get_user_assignments(message.from_user.id, 'lab')
    if not assignments:
        await message.answer("У вас пока нет добавленных лабораторных работ!", reply_markup=main_menu_keyboard)
        return

    text = "📚 Список ваших лабораторных работ:\n\n"
    now = datetime.now()
    
    for lab in sorted(assignments, key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')):
        time_left = datetime.strptime(lab[4], '%Y-%m-%d %H:%M:%S') - now
        deadline_status = "✅ Активно" if time_left.total_seconds() > 0 else "❌ Просрочено"
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        try:
            status = AssignmentStatus(lab[5])
        except ValueError:
            status = AssignmentStatus.NOT_STARTED
            
        status_emoji = {
            AssignmentStatus.NOT_STARTED: "⏳",
            AssignmentStatus.IN_PROGRESS: "🔄",
            AssignmentStatus.COMPLETED: "✅",
            AssignmentStatus.SUBMITTED: "📤"
        }[status]
        
        subject_text = f"Предмет: {get_subject_name(lab[7])}\n" if lab[7] else ""
        
        text += (
            f"🔬 {lab[2]}\n"
            f"{subject_text}"
            f"Описание: {lab[3]}\n"
            f"Статус дедлайна: {deadline_status}\n"
            f"Статус работы: {status_emoji} {get_status_text(status)}\n"
            f"Дедлайн: {datetime.strptime(lab[4], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')}\n"
        )
        if time_left.total_seconds() > 0:
            text += f"Осталось: {days_left}д {hours_left}ч\n"
        text += "\n"

    await message.answer(text, reply_markup=main_menu_keyboard)

@router.message(F.text == "📖 Домашние задания")
async def handle_homework(message: Message):
    assignments = get_user_assignments(message.from_user.id, 'homework')
    if not assignments:
        await message.answer("У вас пока нет добавленных домашних заданий!", reply_markup=main_menu_keyboard)
        return

    text = "📖 Список ваших домашних заданий:\n\n"
    now = datetime.now()
    
    for hw in sorted(assignments, key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')):
        time_left = datetime.strptime(hw[4], '%Y-%m-%d %H:%M:%S') - now
        status = "✅ Активно" if time_left.total_seconds() > 0 else "❌ Просрочено"
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        text += (
            f"📚 {hw[2]}\n"
            f"Статус: {status}\n"
            f"Описание: {hw[3]}\n"
            f"Дедлайн: {datetime.strptime(hw[4], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')}\n"
        )
        if time_left.total_seconds() > 0:
            text += f"Осталось: {days_left}д {hours_left}ч\n"
        text += "\n"

    await message.answer(text, reply_markup=main_menu_keyboard)

@router.message(F.text == "🏆 Рейтинг")
async def handle_rating(message: Message):
    await message.answer("В разработке 🏗", reply_markup=main_menu_keyboard)

@router.message(F.text == "🛠 Управление лабораторными")
async def handle_management(message: Message):
    await message.answer(
        "Меню управления заданиями:\n\n"
        "• Добавить задание - создание нового задания\n"
        "• Список заданий - просмотр всех заданий\n"
        "• Активные дедлайны - просмотр заданий с активными дедлайнами",
        reply_markup=get_assignments_menu_kb()
    )

@router.message(F.text == "📅 Мероприятия")
async def handle_events(message: Message):
    await message.answer(
        "Меню мероприятий:\n\n"
        "• Добавить мероприятие - создание нового мероприятия\n"
        "• Список мероприятий - просмотр всех мероприятий\n"
        "• Ближайшие мероприятия - просмотр предстоящих мероприятий",
        reply_markup=get_events_menu_kb()
    )

@router.message(F.text == "Не нажимать❗❗❗")
async def handle_danger_button(message: Message):
    await message.answer("⚠️ Внимание! Эта кнопка находится в разработке. Пожалуйста, не нажимайте на нее.", reply_markup=main_menu_keyboard)
