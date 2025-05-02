from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import uuid

from states.event_states import EventStates
from keyboards.events_menu import get_events_menu_kb, get_event_actions_kb
from keyboards.main_menu import main_menu_keyboard
from database.db import add_event, get_user_events, update_event, delete_event

router = Router()

@router.callback_query(F.data == "event:add")
async def start_event_adding(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Введите название мероприятия:",
        reply_markup=None
    )
    await state.set_state(EventStates.entering_name)

@router.message(StateFilter(EventStates.entering_name))
async def process_event_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "Введите описание мероприятия:",
        reply_markup=None
    )
    await state.set_state(EventStates.entering_description)

@router.message(StateFilter(EventStates.entering_description))
async def process_event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        "Введите дату и время мероприятия в формате ДД.ММ.ГГГГ ЧЧ:ММ\n"
        "Например: 31.12.2024 15:00",
        reply_markup=None
    )
    await state.set_state(EventStates.entering_date)

@router.message(StateFilter(EventStates.entering_date))
async def process_event_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        data = await state.get_data()
        
        # Добавляем мероприятие в базу данных
        add_event(
            user_id=message.from_user.id,
            title=data["name"],
            description=data["description"],
            event_date=date
        )
        
        await message.answer(
            f"Мероприятие успешно добавлено!\n\n"
            f"Название: {data['name']}\n"
            f"Описание: {data['description']}\n"
            f"Дата: {date.strftime('%d.%m.%Y %H:%M')}",
            reply_markup=get_events_menu_kb()
        )
        await state.clear()
        
    except ValueError:
        await message.answer(
            "Неверный формат даты. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Например: 31.12.2024 15:00"
        )

@router.callback_query(F.data == "event:list")
async def list_events(callback: CallbackQuery):
    events = get_user_events(callback.from_user.id)
    
    if not events:
        await callback.message.edit_text(
            "У вас пока нет добавленных мероприятий!",
            reply_markup=get_events_menu_kb()
        )
        return

    text = "📅 Ваши мероприятия:\n\n"
    now = datetime.now()
    
    for event in sorted(events, key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')):
        time_left = datetime.strptime(event[4], '%Y-%m-%d %H:%M:%S') - now
        status = "✅ Активно" if time_left.total_seconds() > 0 else "❌ Прошло"
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        
        text += (
            f"📌 {event[2]}\n"
            f"Статус: {status}\n"
            f"Описание: {event[3]}\n"
            f"Дата: {datetime.strptime(event[4], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')}\n"
        )
        if time_left.total_seconds() > 0:
            text += f"Осталось: {days_left}д {hours_left}ч\n"
        text += "\n"

    await callback.message.edit_text(
        text,
        reply_markup=get_events_menu_kb()
    )

@router.callback_query(F.data.startswith("event:delete:"))
async def delete_event_handler(callback: CallbackQuery):
    event_id = int(callback.data.split(":")[2])
    
    # Удаляем мероприятие из базы данных
    delete_event(event_id, callback.from_user.id)
    
    await callback.message.edit_text(
        "Мероприятие успешно удалено!",
        reply_markup=get_events_menu_kb()
    )

@router.callback_query(F.data == "event:back")
async def handle_back(callback: CallbackQuery):
    await callback.message.edit_text(
        "Меню мероприятий:\n\n"
        "• Добавить мероприятие - создание нового мероприятия\n"
        "• Просмотр мероприятий - список всех мероприятий",
        reply_markup=get_events_menu_kb()
    ) 