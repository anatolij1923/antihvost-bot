from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Database

router = Router()
db = Database()

class AuthStates(StatesGroup):
    waiting_for_name = State()
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

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if await db.is_authorized(message.from_user.id):
        await message.answer(
            "Вы уже авторизованы!",
            reply_markup=get_main_keyboard()
        )
        return
    
    await message.answer("Добро пожаловать! Для начала работы, пожалуйста, введите ваше ФИО:")
    await state.set_state(AuthStates.waiting_for_name)

@router.message(AuthStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    # Проверяем формат ФИО (должно быть 3 слова)
    name_parts = message.text.split()
    if len(name_parts) != 3:
        await message.answer("Пожалуйста, введите ФИО в формате: Иванов Иван Иванович")
        return
    
    await state.update_data(full_name=message.text)
    await message.answer("Теперь введите номер вашей группы (например, ИВТб-1303-05-00):")
    await state.set_state(AuthStates.waiting_for_group)

@router.message(AuthStates.waiting_for_group)
async def process_group(message: Message, state: FSMContext):
    # Проверяем формат группы
    if not message.text or len(message.text) < 5:  # Простая проверка
        await message.answer("Пожалуйста, введите корректный номер группы (например, ИВТб-1303-05-00)")
        return
    
    user_data = await state.get_data()
    full_name = user_data["full_name"]
    group_name = message.text
    
    await db.add_student(message.from_user.id, full_name, group_name)
    await state.clear()
    
    await message.answer(
        f"Спасибо! Вы успешно авторизованы.\n"
        f"ФИО: {full_name}\n"
        f"Группа: {group_name}\n\n"
        f"Теперь вы можете использовать бота для учета лабораторных работ.",
        reply_markup=get_main_keyboard()
    )

# Обработчик кнопки "Моя информация"
@router.message(F.text == "👤 Моя информация")
async def show_user_info(message: Message):
    student = await db.get_student(message.from_user.id)
    if not student:
        await message.answer("Вы не авторизованы. Пожалуйста, используйте команду /start")
        return
    
    await message.answer(
        f"👤 Ваша информация:\n\n"
        f"ФИО: {student.full_name}\n"
        f"Группа: {student.group_name}\n"
        f"ID: {student.user_id}"
    ) 