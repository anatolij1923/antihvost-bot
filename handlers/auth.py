from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Database
from handlers.menu import get_main_menu_reply_keyboard, cmd_menu
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from services.group_tasks import GroupTasksManager

router = Router()
db = Database()
group_tasks_manager = GroupTasksManager(db)

GROUP_REGEX = r"^[А-ЯЁ]{3,4}б?-\d{4}-\d{2}-\d{2}$"

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
    group_name_raw = message.text
    
    group_name_raw = message.text
    
    # Нормализация ввода
    # Удаляем лишние пробелы и заменяем пробелы на дефисы
    cleaned_name = group_name_raw.strip().replace(" ", "-")
    
    # Разбиваем на части по дефису
    parts = cleaned_name.split("-")
    
    # Проверяем, что есть хотя бы одна часть
    if not parts:
        await message.answer(
            "❌ Неверный формат группы. Пожалуйста, введите группу в правильном формате, например, ИВТб-1303-05-00"
        )
        return
    
    # Обрабатываем первую часть (направление и опционально 'б')
    first_part = parts[0]
    normalized_first_part = ""
    if first_part:
        # Капитализируем буквы направления
        normalized_first_part = first_part[:-1].upper() + first_part[-1].lower() if first_part[-1].lower() == 'б' and len(first_part) > 1 else first_part.upper()
    
    # Собираем нормализованное имя группы
    group_name_normalized = normalized_first_part + "-" + "-".join(parts[1:])
    
    # Валидация нормализованного ввода
    if not re.match(GROUP_REGEX, group_name_normalized):
        await message.answer(
            "❌ Неверный формат группы. Пожалуйста, введите группу в правильном формате, например, ИВТб-1303-05-00"
        )
        # Остаемся в текущем состоянии, чтобы пользователь мог ввести группу снова
        return
    
    # Получаем сохраненные данные
    data = await state.get_data()
    full_name = data.get("full_name")
    
    # Добавляем студента в базу данных с нормализованным именем группы
    if await db.add_student(message.from_user.id, full_name, group_name_normalized):
        # Добавляем лабораторные работы для студентов ИВТб 1 курса (используем нормализованное имя)
        if group_name_normalized.startswith("ИВТб-1"): # Используем lowercase 'б' here
            await group_tasks_manager.add_labs_for_new_student(message.from_user.id, group_name_normalized)
        
        await message.answer(
            f"✅ Авторизация успешно завершена!\n\n"
            f"👤 Ваше имя: {full_name}\n"
            f"👥 Ваша группа: {group_name_normalized}\n\n"
            "Теперь вы можете использовать все функции бота."
        )
        # Вызываем команду /menu после успешной авторизации
        await cmd_menu(message)
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
