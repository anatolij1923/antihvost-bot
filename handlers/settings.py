from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.database import Database
from keyboards.menu import get_settings_keyboard, get_main_keyboard
from keyboards.settings import get_notifications_keyboard

router = Router()
db = Database()

@router.message(Command("settings"))
async def settings(message: Message):
    """Обработчик команды /settings"""
    await message.answer(
        "⚙️ Настройки",
        reply_markup=get_settings_keyboard()
    )

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

@router.callback_query(F.data == "notifications")
async def notifications_settings(callback: CallbackQuery):
    """Обработчик настройки уведомлений"""
    is_enabled = await db.are_notifications_enabled(callback.from_user.id)
    status = "✅ Включены" if is_enabled else "❌ Выключены"
    
    await callback.message.edit_text(
        f"🔔 Настройки уведомлений\n\n"
        f"Текущий статус: {status}\n\n"
        f"Вы можете включить или выключить уведомления о предстоящих дедлайнах.",
        reply_markup=get_notifications_keyboard(is_enabled)
    )

@router.callback_query(F.data == "toggle_notifications")
async def toggle_notifications(callback: CallbackQuery):
    """Обработчик переключения уведомлений"""
    new_state = await db.toggle_notifications(callback.from_user.id)
    status = "✅ Включены" if new_state else "❌ Выключены"
    
    await callback.message.edit_text(
        f"🔔 Настройки уведомлений\n\n"
        f"Текущий статус: {status}\n\n"
        f"Вы можете включить или выключить уведомления о предстоящих дедлайнах.",
        reply_markup=get_notifications_keyboard(new_state)
    )

@router.callback_query(lambda c: c.data == "support")
async def handle_support(callback: CallbackQuery):
    await callback.answer("Бог вам в помощь 🙏")

@router.callback_query(lambda c: c.data == "back_to_main")
async def handle_back(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(F.data == "back_to_settings")
async def back_to_settings(callback: CallbackQuery):
    """Обработчик возврата к основным настройкам"""
    await callback.message.edit_text(
        "⚙️ Настройки",
        reply_markup=get_settings_keyboard()
    ) 