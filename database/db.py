import sqlite3
import os
from pathlib import Path
from datetime import datetime

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
        status TEXT DEFAULT 'not_started',  -- Значение по умолчанию соответствует AssignmentStatus.NOT_STARTED
        type TEXT NOT NULL,  -- 'lab' или 'homework'
        subject TEXT,  -- для лабораторных работ
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

def add_assignment(user_id: int, title: str, description: str, due_date: datetime, assignment_type: str, subject: str = None):
    """Добавляет новое задание в базу данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO assignments (user_id, title, description, due_date, type, subject, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, title, description, due_date, assignment_type, subject, 'not_started'))
    
    conn.commit()
    conn.close()

def get_user_assignments(user_id: int, assignment_type: str = None):
    """Получает все задания пользователя, опционально фильтруя по типу"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if assignment_type:
        cursor.execute('''
        SELECT * FROM assignments 
        WHERE user_id = ? AND type = ?
        ORDER BY due_date
        ''', (user_id, assignment_type))
    else:
        cursor.execute('''
        SELECT * FROM assignments 
        WHERE user_id = ?
        ORDER BY due_date
        ''', (user_id,))
    
    assignments = cursor.fetchall()
    conn.close()
    return assignments

def update_assignment_status(assignment_id: int, user_id: int, new_status: str):
    """Обновляет статус задания, проверяя права доступа"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE assignments 
    SET status = ?
    WHERE id = ? AND user_id = ?
    ''', (new_status, assignment_id, user_id))
    
    conn.commit()
    conn.close()

def delete_assignment(assignment_id: int, user_id: int):
    """Удаляет задание, проверяя права доступа"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM assignments 
    WHERE id = ? AND user_id = ?
    ''', (assignment_id, user_id))
    
    conn.commit()
    conn.close()

def add_event(user_id: int, title: str, description: str, event_date: str):
    """Добавляет новое мероприятие в базу данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO events (user_id, title, description, event_date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, title, description, event_date))
    
    conn.commit()
    conn.close()

def get_user_events(user_id: int):
    """Получает все мероприятия пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM events 
    WHERE user_id = ?
    ORDER BY event_date
    ''', (user_id,))
    
    events = cursor.fetchall()
    conn.close()
    return events

def update_event(event_id: int, user_id: int, title: str, description: str, event_date: str):
    """Обновляет мероприятие, проверяя права доступа"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE events 
    SET title = ?, description = ?, event_date = ?
    WHERE id = ? AND user_id = ?
    ''', (title, description, event_date, event_id, user_id))
    
    conn.commit()
    conn.close()

def delete_event(event_id: int, user_id: int):
    """Удаляет мероприятие, проверяя права доступа"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM events 
    WHERE id = ? AND user_id = ?
    ''', (event_id, user_id))
    
    conn.commit()
    conn.close() 