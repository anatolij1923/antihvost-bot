from datetime import datetime, timedelta
import asyncio
from database.database import Database
from aiogram import Bot

class NotificationManager:
    def __init__(self, db: Database, bot: Bot):
        self.db = db
        self.bot = bot
        self.notification_intervals = [7, 3, 1]  # дни до дедлайна для уведомлений
        print("NotificationManager инициализирован")

    async def check_deadlines(self):
        print("Запуск системы уведомлений...")
        while True:
            try:
                current_date = datetime.now()
                print(f"\nПроверка уведомлений в {current_date.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Получаем всех авторизованных пользователей
                self.db.cursor.execute('SELECT user_id FROM users WHERE is_authorized = TRUE AND notifications_enabled = TRUE')
                authorized_users = self.db.cursor.fetchall()
                print(f"Найдено авторизованных пользователей с включенными уведомлениями: {len(authorized_users)}")
                
                for user in authorized_users:
                    user_id = user[0]
                    # print(f"\nПроверка задач для пользователя {user_id}")
                    
                    for days in self.notification_intervals:
                        target_date = current_date + timedelta(days=days)
                        # print(f"Проверка задач на {target_date.strftime('%Y-%m-%d')} (через {days} дней)")
                        
                        tasks = await self.db.get_tasks_by_date(target_date, user_id)
                        # print(f"Найдено задач: {len(tasks)}")
                        
                        for task in tasks:
                            task_id = task[0]
                            task_title = task[1]
                            task_type = task[2]
                            subject = task[3]
                            deadline = task[4]
                            priority = task[6]
                            
                            print(f"Отправка уведомления о задаче: {task_title}")
                            
                            # Формируем сообщение с эмодзи в зависимости от типа задачи
                            emoji = "📝"  # По умолчанию
                            if task_type == "🔬 Лабораторная":
                                emoji = "🔬"
                            elif task_type == "📚 Домашнее задание":
                                emoji = "📚"
                            elif task_type == "📊 Проект":
                                emoji = "📊"
                            
                            # Формируем сообщение с эмодзи приоритета
                            priority_emoji = "⚪"  # По умолчанию
                            if priority == "🔴 Высокий":
                                priority_emoji = "🔴"
                            elif priority == "🟡 Средний":
                                priority_emoji = "🟡"
                            elif priority == "🟢 Низкий":
                                priority_emoji = "🟢"
                            
                            message = f"🔔 Напоминание!\n\n" \
                                    f"{emoji} {task_type}\n" \
                                    f"📚 Предмет: {subject}\n" \
                                    f"📌 Задача: {task_title}\n" \
                                    f"{priority_emoji} Приоритет: {priority}\n" \
                                    f"⏰ До дедлайна осталось: {days} дней\n" \
                                    f"📅 Срок сдачи: {deadline}"
                            
                            try:
                                await self.bot.send_message(user_id, message)
                                print(f"Уведомление успешно отправлено пользователю {user_id}")
                            except Exception as e:
                                print(f"Ошибка отправки уведомления пользователю {user_id}: {e}")
                
                # print("Ожидание следующей проверки...")
                await asyncio.sleep(6 * 60 * 60)
                
            except Exception as e:
                print(f"Критическая ошибка в системе уведомлений: {e}")
                await asyncio.sleep(60)  # При ошибке ждем минуту перед следующей попыткой 