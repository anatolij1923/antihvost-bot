from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import Database

router = Router()
db = Database()

@router.message(Command("rating"))
async def show_rating_menu(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Мой рейтинг", callback_data="my_rating")],
            [InlineKeyboardButton(text="🏆 Топ студентов", callback_data="top_students")]
        ]
    )
    await message.answer("Выберите раздел рейтинга:", reply_markup=keyboard)

@router.callback_query(F.data == "my_rating")
async def show_my_rating(callback: CallbackQuery):
    user_id = callback.from_user.id
    rating = await db.get_user_rating(user_id)
    rank = await db.get_user_rank(user_id)
    total_users = await db.get_total_users()
    
    text = f"📊 Твой рейтинг: {rating} очков\n📈 Место в рейтинге: {rank} из {total_users}"
    await callback.message.edit_text(text)

@router.callback_query(F.data == "top_students")
async def show_top_students(callback: CallbackQuery):
    top_students = await db.get_top_students(5)
    
    text = "🏆 Топ студентов:\n\n"
    for i, student in enumerate(top_students, 1):
        text += f"{i}. {student['name']} - {student['rating']} очков\n"
    
    await callback.message.edit_text(text) 