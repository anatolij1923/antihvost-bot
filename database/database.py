import sqlite3
from datetime import datetime
from dataclasses import dataclass
import os

@dataclass
class Student:
    user_id: int
    full_name: str
    group_name: str
    notifications_enabled: bool

class Database:
    def __init__(self):
        # Создаем директорию для базы данных, если её нет
        os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
        # Указываем путь к базе данных в директории database/
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bot.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    async def _create_tables(self):
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                full_name TEXT,
                group_name TEXT,
                is_authorized BOOLEAN DEFAULT FALSE,
                notifications_enabled BOOLEAN DEFAULT TRUE
            )
        ''')

        # Таблица задач
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                task_type TEXT NOT NULL,
                subject TEXT NOT NULL,
                deadline DATETIME,
                description TEXT,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                lab_status TEXT DEFAULT 'not_started',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        self.conn.commit()

    async def is_authorized(self, user_id: int) -> bool:
        self.cursor.execute('SELECT is_authorized FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    async def add_task(self, user_id: int, title: str, task_type: str, subject: str, 
                      deadline: datetime, description: str, priority: str) -> bool:
        try:
            self.cursor.execute('''
                INSERT INTO tasks (user_id, title, task_type, subject, deadline, description, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, title, task_type, subject, deadline, description, priority))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding task: {e}")
            return False 

    async def get_user_tasks(self, user_id: int) -> list:
        try:
            self.cursor.execute('''
                SELECT id, title, task_type, subject, 
                       strftime('%d.%m.%Y %H:%M', deadline) as deadline,
                       description, priority, status, lab_status
                FROM tasks
                WHERE user_id = ? AND status = 'active'
                ORDER BY deadline ASC
            ''', (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting user tasks: {e}")
            return []

    async def add_student(self, user_id: int, full_name: str, group_name: str) -> bool:
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, full_name, group_name, is_authorized, notifications_enabled)
                VALUES (?, ?, ?, TRUE, TRUE)
            ''', (user_id, full_name, group_name))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False

    async def get_student(self, user_id: int) -> Student | None:
        try:
            self.cursor.execute('''
                SELECT user_id, full_name, group_name, notifications_enabled
                FROM users
                WHERE user_id = ? AND is_authorized = TRUE
            ''', (user_id,))
            result = self.cursor.fetchone()
            if result:
                return Student(user_id=result[0], full_name=result[1], group_name=result[2], notifications_enabled=result[3])
            return None
        except Exception as e:
            print(f"Error getting student: {e}")
            return None 

    async def update_lab_status(self, task_id: int, status: str) -> bool:
        try:
            self.cursor.execute('''
                UPDATE tasks
                SET lab_status = ?
                WHERE id = ? AND task_type = '🔬 Лабораторная'
            ''', (status, task_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating lab status: {e}")
            return False 

    async def get_tasks_by_date(self, date: datetime, user_id: int) -> list:
        try:
            self.cursor.execute('''
                SELECT id, title, task_type, subject, 
                       strftime('%d.%m.%Y %H:%M', deadline) as deadline,
                       description, priority, status, lab_status
                FROM tasks
                WHERE date(deadline) = date(?) 
                AND user_id = ?
                AND status = 'active'
                ORDER BY deadline ASC
            ''', (date, user_id))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting tasks by date: {e}")
            return []

    async def get_tasks_by_date_range(self, start_date: datetime, end_date: datetime, user_id: int) -> list:
        try:
            self.cursor.execute('''
                SELECT id, title, task_type, subject, 
                       strftime('%d.%m.%Y %H:%M', deadline) as deadline,
                       description, priority, status, lab_status
                FROM tasks
                WHERE date(deadline) BETWEEN date(?) AND date(?)
                AND user_id = ?
                AND status = 'active'
                ORDER BY deadline ASC
            ''', (start_date, end_date, user_id))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting tasks by date range: {e}")
            return []

    async def toggle_notifications(self, user_id: int) -> bool:
        try:
            # Получаем текущее состояние уведомлений
            self.cursor.execute('SELECT notifications_enabled FROM users WHERE user_id = ?', (user_id,))
            current_state = self.cursor.fetchone()
            if not current_state:
                return False
            
            new_state = not current_state[0]
            self.cursor.execute('''
                UPDATE users
                SET notifications_enabled = ?
                WHERE user_id = ?
            ''', (new_state, user_id))
            self.conn.commit()
            return new_state
        except Exception as e:
            print(f"Error toggling notifications: {e}")
            return False

    async def are_notifications_enabled(self, user_id: int) -> bool:
        try:
            self.cursor.execute('SELECT notifications_enabled FROM users WHERE user_id = ?', (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else False
        except Exception as e:
            print(f"Error checking notifications status: {e}")
            return False 