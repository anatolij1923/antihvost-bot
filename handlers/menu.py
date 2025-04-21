from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import main_menu_keyboard
from keyboards.lab_menu import get_assignments_menu_kb
from keyboards.events_menu import events_menu_keyboard
from utils.storage import get_authorized_user_name
from datetime import datetime

router = Router()

@router.message(F.text == "📚 Просмотр лабораторных")
async def handle_labs_view(message: Message):
    from handlers.assignments import assignments  # импортируем словарь с заданиями
    
    labs = {k: v for k, v in assignments.items() if v.type == 'lab'}
    if not labs:
        await message.answer("Пока нет добавленных лабораторных работ!", reply_markup=main_menu_keyboard)
        return

    text = "📚 Список лабораторных работ:\n\n"
    now = datetime.now()
    
    for lab in sorted(labs.values(), key=lambda x: x.deadline):
        time_left = lab.deadline - now
        status = "✅ Активно" if time_left.total_seconds() > 0 else "❌ Просрочено"
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        text += (
            f"🔬 {lab.name}\n"
            f"Статус: {status}\n"
            f"Описание: {lab.description}\n"
            f"Дедлайн: {lab.deadline.strftime('%d.%m.%Y %H:%M')}\n"
        )
        if time_left.total_seconds() > 0:
            text += f"Осталось: {days_left}д {hours_left}ч\n"
        text += "\n"

    await message.answer(text, reply_markup=main_menu_keyboard)

@router.message(F.text == "📖 Домашние задания")
async def handle_homework(message: Message):
    from handlers.assignments import assignments  # импортируем словарь с заданиями
    
    homeworks = {k: v for k, v in assignments.items() if v.type == 'homework'}
    if not homeworks:
        await message.answer("Пока нет добавленных домашних заданий!", reply_markup=main_menu_keyboard)
        return

    text = "📖 Список домашних заданий:\n\n"
    now = datetime.now()
    
    for hw in sorted(homeworks.values(), key=lambda x: x.deadline):
        time_left = hw.deadline - now
        status = "✅ Активно" if time_left.total_seconds() > 0 else "❌ Просрочено"
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        text += (
            f"📚 {hw.name}\n"
            f"Статус: {status}\n"
            f"Описание: {hw.description}\n"
            f"Дедлайн: {hw.deadline.strftime('%d.%m.%Y %H:%M')}\n"
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

@router.message(F.text == "Не нажимать❗❗❗")
async def handle_danger_button(message: Message):
    name = get_authorized_user_name(message.from_user.id)
    await message.answer(
        f"Поздравляем 🥳🥳🥳. {name}, тебе русским языком было сказано \"Не нажимать\", "
        f"теперь на твое имя было отправлено заявление об отчислении Репкину Дмитрию Александровичу",
        reply_markup=main_menu_keyboard
    )

@router.message(F.text == "📅 Мероприятия")
async def handle_events(message: Message):
    await message.answer(
        "Меню мероприятий:\n\n"
        "• Добавить мероприятие - создание нового мероприятия\n"
        "• Просмотр мероприятий - список всех мероприятий",
        reply_markup=events_menu_keyboard
    )

@router.message(F.text == "Добавить мероприятие")
async def handle_add_event(message: Message):
    await message.answer("Функционал добавления мероприятий в разработке 🏗", reply_markup=events_menu_keyboard)

@router.message(F.text == "Просмотр мероприятий")
async def handle_view_events(message: Message):
    await message.answer("Функционал просмотра мероприятий в разработке 🏗", reply_markup=events_menu_keyboard)

@router.message(F.text == "Назад")
async def handle_back(message: Message):
    await message.answer("Главное меню", reply_markup=main_menu_keyboard)
