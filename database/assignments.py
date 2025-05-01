from .db import get_connection
from datetime import datetime

def add_assignment(user_id: int, title: str, description: str = None, due_date: datetime = None):
    """Добавляет новое задание в базу данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO assignments (user_id, title, description, due_date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, title, description, due_date))
    
    conn.commit()
    conn.close()

def get_user_assignments(user_id: int):
    """Получает все задания пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM assignments 
    WHERE user_id = ? 
    ORDER BY created_at DESC
    ''', (user_id,))
    
    assignments = cursor.fetchall()
    conn.close()
    return assignments

def update_assignment_status(assignment_id: int, status: str):
    """Обновляет статус задания"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE assignments 
    SET status = ? 
    WHERE id = ?
    ''', (status, assignment_id))
    
    conn.commit()
    conn.close()

def delete_assignment(assignment_id: int):
    """Удаляет задание"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))
    
    conn.commit()
    conn.close() 