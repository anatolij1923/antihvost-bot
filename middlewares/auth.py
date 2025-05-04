from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from database.database import Database
from aiogram.fsm.context import FSMContext
from handlers.auth import AuthStates

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Получаем состояние из данных
        state: FSMContext = data.get('state')
        
        # Пропускаем команду /start и /auth
        if isinstance(event, Message):
            if event.text and (event.text.startswith('/start') or event.text.startswith('/auth')):
                return await handler(event, data)
        
        # Пропускаем сообщения во время процесса авторизации
        if state:
            current_state = await state.get_state()
            if current_state in [AuthStates.waiting_for_full_name.state, AuthStates.waiting_for_group.state]:
                return await handler(event, data)
        
        # Проверяем авторизацию пользователя
        db = Database()
        if not await db.is_authorized(event.from_user.id):
            # Если пользователь не авторизован, отправляем сообщение
            if isinstance(event, Message):
                await event.answer(
                    "⚠️ Для использования бота необходимо авторизоваться.\n\n"
                    "Пожалуйста, используйте команду /auth для авторизации."
                )
            else:  # CallbackQuery
                await event.answer(
                    "⚠️ Для использования бота необходимо авторизоваться.\n\n"
                    "Пожалуйста, используйте команду /auth для авторизации.",
                    show_alert=True
                )
            return
        
        # Если пользователь авторизован, продолжаем обработку
        return await handler(event, data) 