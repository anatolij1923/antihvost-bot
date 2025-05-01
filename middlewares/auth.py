from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any, Callable, Awaitable
from aiogram.fsm.context import FSMContext
from states.auth_states import AuthStates
from database.db import get_connection, get_user_fullname

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
        if (is_user_authorized(user_id) or 
            event.text and event.text.startswith('/start') or 
            current_state in [AuthStates.waiting_for_fullname, AuthStates.waiting_for_group]):
            return await handler(event, data)
        
        # В остальных случаях требуем авторизацию
        await event.answer("Пожалуйста, авторизуйтесь с помощью команды /start")
        return

def authorize_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None, fullname: str = None, group_name: str = None):
    """Авторизует пользователя и сохраняет его данные в базу данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Проверяем, существует ли пользователь
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        # Если пользователь не существует, добавляем его
        cursor.execute('''
        INSERT INTO users (user_id, username, first_name, last_name, fullname, group_name)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, fullname, group_name))
    else:
        # Если пользователь существует, обновляем его данные
        cursor.execute('''
        UPDATE users 
        SET username = ?, first_name = ?, last_name = ?, fullname = ?, group_name = ?
        WHERE user_id = ?
        ''', (username, first_name, last_name, fullname, group_name, user_id))
    
    conn.commit()
    conn.close()

def is_user_authorized(user_id: int) -> bool:
    """Проверяет, авторизован ли пользователь"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    is_authorized = cursor.fetchone() is not None
    
    conn.close()
    return is_authorized 