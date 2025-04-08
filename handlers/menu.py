from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import main_menu_keyboard
from utils.storage import get_authorized_user_name

router = Router()

@router.message(F.text == "📚 Просмотр лабораторных")
async def handle_labs_view(message: Message):
    await message.answer("В разработке 🏗", reply_markup=main_menu_keyboard)

@router.message(F.text == "📖 Домашние задания")
async def handle_homework(message: Message):
    await message.answer("В разработке 🏗", reply_markup=main_menu_keyboard)

@router.message(F.text == "🏆 Рейтинг")
async def handle_rating(message: Message):
    await message.answer("В разработке 🏗", reply_markup=main_menu_keyboard)

@router.message(F.text == "🛠 Управление лабораторными")
async def handle_management(message: Message):
    await message.answer("В разработке 🏗", reply_markup=main_menu_keyboard)

@router.message(F.text == "Не нажимать❗❗❗")
async def handle_danger_button(message: Message):
    name = get_authorized_user_name(message.from_user.id)
    await message.answer(
        f"Поздравляем 🥳🥳🥳. {name}, тебе русским языком было сказано \"Не нажимать\", "
        f"теперь на твое имя было отправлено заявление об отчислении Репкину Дмитрию Александровичу",
        reply_markup=main_menu_keyboard
    )
