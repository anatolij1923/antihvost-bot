from typing import Any, Dict
from aiogram.types import Message

async def get_user_data(message: Message) -> Dict[str, Any]:
    """Получение данных пользователя"""
    return {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name
    }

__all__ = ['get_user_data'] 