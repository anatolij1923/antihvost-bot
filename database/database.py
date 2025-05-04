import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('bot.db')
        self.cursor = self.conn.cursor()

    async def _create_tables(self):
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                is_authorized BOOLEAN DEFAULT FALSE
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