from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import cancel_keyboard, main_menu_keyboard
from states.auth_states import AuthStates
from middlewares.auth import authorize_user, is_user_authorized
import re
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    # Если пользователь уже авторизован, показываем главное меню
    if is_user_authorized(message.from_user.id):
        await message.answer("Вы уже авторизованы. Используйте /menu для перехода в главное меню.", 
                           reply_markup=main_menu_keyboard)
        return
    
    # Если не авторизован, начинаем процесс авторизации
    await message.answer("Введите ваше ФИО:", reply_markup=cancel_keyboard)
    await state.set_state(AuthStates.waiting_for_fullname)

@router.message(AuthStates.waiting_for_fullname)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Теперь введите номер группы (например, ИВТб-1303-05-00):")
    await state.set_state(AuthStates.waiting_for_group)

@router.message(AuthStates.waiting_for_group)
async def process_group(message: Message, state: FSMContext):
    group_pattern = r"^ИВТб-[1-4]30[1-7]-0[4-6]-00$"
    if not re.match(group_pattern, message.text):
        await message.answer("Неверный формат группы. Попробуйте снова:")
        return
    
    data = await state.get_data()
    fullname = data["fullname"]
    group = message.text
    
    # Авторизуем пользователя и сохраняем его данные в базу данных
    authorize_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        fullname=fullname,
        group_name=group
    )
    
    await message.answer(f"Вы авторизованы как {fullname} из группы {group}", reply_markup=main_menu_keyboard)
    await state.clear()
