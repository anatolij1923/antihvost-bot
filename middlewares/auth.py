from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any, Callable, Awaitable
from aiogram.fsm.context import FSMContext
from states.auth_states import AuthStates

# Временное хранилище для авторизованных пользователей
authorized_users = set()

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        state: FSMContext = data.get('state')
        
        # Получаем текущее состояние пользователя
        current_state = await state.get_state() if state else None
        
        # Разрешаем все сообщения, если:
        # 1. Пользователь авторизован
        # 2. Это команда /start
        # 3. Пользователь находится в процессе авторизации
        if (user_id in authorized_users or 
            event.text and event.text.startswith('/start') or 
            current_state in [AuthStates.waiting_for_fullname, AuthStates.waiting_for_group]):
            return await handler(event, data)
        
        # В остальных случаях требуем авторизацию
        await event.answer("Пожалуйста, авторизуйтесь с помощью команды /start")
        return

# Функция для авторизации пользователя
def authorize_user(user_id: int):
    authorized_users.add(user_id)

# Функция для проверки, авторизован ли пользователь
def is_user_authorized(user_id: int) -> bool:
    return user_id in authorized_users 