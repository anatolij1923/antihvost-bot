from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from database import Database

class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        self.db = Database()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Пропускаем команду /start и сообщения в процессе авторизации
        if event.text == "/start" or "state" in data:
            return await handler(event, data)

        # Проверяем авторизацию
        if not await self.db.is_authorized(event.from_user.id):
            await event.answer("Пожалуйста, авторизуйтесь с помощью команды /start")
            return
        
        return await handler(event, data) 