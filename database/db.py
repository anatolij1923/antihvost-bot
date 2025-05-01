import sqlite3
import os
from pathlib import Path

# Путь к файлу базы данных
DB_PATH = Path(__file__).parent / 'bot.db'

def get_connection():
    """Создает и возвращает соединение с базой данных"""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Инициализирует базу данных, создает необходимые таблицы"""
    conn = get_connection()
    cursor = conn.cursor()

    # Создаем таблицу пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        fullname TEXT,
        group_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Создаем таблицу заданий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        due_date TIMESTAMP,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    # Создаем таблицу событий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        event_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    conn.commit()
    conn.close()

def add_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None, fullname: str = None, group_name: str = None):
    """Добавляет нового пользователя в базу данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, fullname, group_name)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, fullname, group_name))
    
    conn.commit()
    conn.close()

def get_user(user_id: int):
    """Получает информацию о пользователе по его ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def get_user_fullname(user_id: int) -> str:
    """Получает полное имя пользователя по его ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT fullname FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None 