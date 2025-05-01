from .db import get_connection
from datetime import datetime

def add_event(user_id: int, title: str, description: str = None, event_date: datetime = None):
    """Добавляет новое событие в базу данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO events (user_id, title, description, event_date)
    VALUES (?, ?, ?, ?)
    ''', (user_id, title, description, event_date))
    
    conn.commit()
    conn.close()

def get_user_events(user_id: int):
    """Получает все события пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM events 
    WHERE user_id = ? 
    ORDER BY event_date ASC
    ''', (user_id,))
    
    events = cursor.fetchall()
    conn.close()
    return events

def get_upcoming_events(user_id: int, days_ahead: int = 7):
    """Получает предстоящие события пользователя на указанное количество дней вперед"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM events 
    WHERE user_id = ? 
    AND event_date BETWEEN datetime('now') AND datetime('now', ? || ' days')
    ORDER BY event_date ASC
    ''', (user_id, days_ahead))
    
    events = cursor.fetchall()
    conn.close()
    return events

def delete_event(event_id: int):
    """Удаляет событие"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    
    conn.commit()
    conn.close() 