from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Database
from handlers.menu import get_main_menu_reply_keyboard
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
db = Database()

class AuthStates(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_group = State()

# Создаем клавиатуру с кнопкой
def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Моя информация")],
        ],
        resize_keyboard=True
    )
    return keyboard

@router.message(Command("auth"))
async def cmd_auth(message: types.Message, state: FSMContext):
    # Проверяем, не авторизован ли уже пользователь
    if await db.is_authorized(message.from_user.id):
        await message.answer(
            "✅ Вы уже авторизованы!\n\n"
            "Если вы хотите изменить свои данные, пожалуйста, обратитесь к администратору."
        )
        return
    
    # Запрашиваем ФИО
    await message.answer(
        "👤 Пожалуйста, введите ваше полное имя (ФИО):"
    )
    await state.set_state(AuthStates.waiting_for_full_name)

@router.message(AuthStates.waiting_for_full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    # Сохраняем ФИО
    await state.update_data(full_name=message.text)
    
    # Запрашиваем группу
    await message.answer(
        "👥 Пожалуйста, введите название вашей группы:"
    )
    await state.set_state(AuthStates.waiting_for_group)

@router.message(AuthStates.waiting_for_group)
async def process_group(message: types.Message, state: FSMContext):
    # Получаем сохраненные данные
    data = await state.get_data()
    full_name = data.get("full_name")
    group_name = message.text
    
    # Добавляем студента в базу данных
    if await db.add_student(message.from_user.id, full_name, group_name):
        await message.answer(
            f"✅ Авторизация успешно завершена!\n\n"
            f"👤 Ваше имя: {full_name}\n"
            f"👥 Ваша группа: {group_name}\n\n"
            "Теперь вы можете использовать все функции бота."
        )
    else:
        await message.answer(
            "❌ Произошла ошибка при авторизации.\n\n"
            "Пожалуйста, попробуйте еще раз или обратитесь к администратору."
        )
    
    # Сбрасываем состояние
    await state.clear()

# Обработчик кнопки "Моя информация"
@router.message(F.text == "👤 Моя информация")
async def show_user_info(message: Message):
    student = await db.get_student(message.from_user.id)
    if not student:
        await message.answer("Вы не авторизованы. Пожалуйста, используйте команду /auth")
        return
    
    await message.answer(
        f"👤 Ваша информация:\n\n"
        f"ФИО: {student.full_name}\n"
        f"Группа: {student.group_name}\n"
        f"ID: {student.user_id}"
    ) 