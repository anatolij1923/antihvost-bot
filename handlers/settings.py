from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from database.database import Database
from keyboards.menu import get_settings_keyboard, get_main_keyboard

router = Router()
db = Database()

@router.callback_query(lambda c: c.data == "settings")
async def handle_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚙️ Настройки",
        reply_markup=get_settings_keyboard()
    )

@router.callback_query(lambda c: c.data == "profile")
async def handle_profile(callback: CallbackQuery):
    student = await db.get_student(callback.from_user.id)
    if not student:
        await callback.answer("Вы не авторизованы. Пожалуйста, используйте команду /start")
        return
    
    await callback.message.edit_text(
        f"👤 Ваш профиль:\n\n"
        f"ФИО: {student.full_name}\n"
        f"Группа: {student.group_name}",
        reply_markup=get_settings_keyboard()
    )

@router.callback_query(lambda c: c.data == "notifications")
async def handle_notifications(callback: CallbackQuery):
    await callback.answer("Функционал уведомлений будет добавлен в ближайшее время")

@router.callback_query(lambda c: c.data == "support")
async def handle_support(callback: CallbackQuery):
    await callback.answer("Бог вам в помощь 🙏")

@router.callback_query(lambda c: c.data == "back_to_main")
async def handle_back(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню",
        reply_markup=get_main_keyboard()
    ) 