from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import cancel_keyboard
from states.auth_states import AuthStates
import re

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Введите ваше ФИО:", reply_markup=cancel_keyboard)
    await state.set_state(AuthStates.waiting_for_fullname)

@router.message(AuthStates.waiting_for_fullname)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Теперь введите номер группы (например, ИВТб-1303-05-00):")
    await state.set_state(AuthStates.waiting_for_group)

@router.message(AuthStates.waiting_for_group)
async def process_group(message: Message, state: FSMContext):
    group_pattern = r"^ИВТб-130[1-9]-05-00$"
    if not re.match(group_pattern, message.text):
        await message.answer("Неверный формат группы. Попробуйте снова:")
        return
    data = await state.get_data()
    fullname = data["fullname"]
    group = message.text
    # Тут будет проверка в БД и сохранение, пока просто выводим
    await message.answer(f"Вы авторизованы как {fullname} из группы {group}")
    await state.clear()
