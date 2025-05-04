from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from database import Database
from keyboards.calendar import get_calendar_keyboard
from keyboards.menu import get_main_keyboard

router = Router()
db = Database()

@router.message(Command("calendar"))
async def show_calendar(message: Message):
    await message.answer(
        "Выберите период для просмотра заданий:",
        reply_markup=get_calendar_keyboard()
    )

@router.callback_query(F.data == "calendar_today")
async def show_today_tasks(callback: CallbackQuery):
    today = datetime.now().date()
    tasks = await db.get_tasks_by_date(today, callback.from_user.id)
    
    if not tasks:
        await callback.message.edit_text(
            "На сегодня нет запланированных заданий",
            reply_markup=get_calendar_keyboard()
        )
        return
    
    text = "📝 Задания на сегодня:\n\n"
    for task in tasks:
        text += f"• {task[1]}\n"
        if task[4]:
            text += f"  Дедлайн: {task[4]}\n"
        text += "\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_calendar_keyboard()
    )

@router.callback_query(F.data == "calendar_week")
async def show_week_tasks(callback: CallbackQuery):
    today = datetime.now().date()
    week_end = today + timedelta(days=7)
    tasks = await db.get_tasks_by_date_range(today, week_end, callback.from_user.id)
    
    if not tasks:
        await callback.message.edit_text(
            "На этой неделе нет запланированных заданий",
            reply_markup=get_calendar_keyboard()
        )
        return
    
    text = "📝 Задания на неделю:\n\n"
    for task in tasks:
        text += f"• {task[1]}\n"
        if task[4]:
            text += f"  Дедлайн: {task[4]}\n"
        text += "\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_calendar_keyboard()
    )

@router.callback_query(F.data == "calendar_month")
async def show_month_tasks(callback: CallbackQuery):
    today = datetime.now().date()
    month_end = today.replace(day=1) + timedelta(days=32)
    month_end = month_end.replace(day=1) - timedelta(days=1)
    tasks = await db.get_tasks_by_date_range(today, month_end, callback.from_user.id)
    
    if not tasks:
        await callback.message.edit_text(
            "В этом месяце нет запланированных заданий",
            reply_markup=get_calendar_keyboard()
        )
        return
    
    text = "📝 Задания на месяц:\n\n"
    for task in tasks:
        text += f"• {task[1]}\n"
        if task[4]:
            text += f"  Дедлайн: {task[4]}\n"
        text += "\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_calendar_keyboard()
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    ) 