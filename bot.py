from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import asyncio
import os
from dotenv import load_dotenv
from database import Database
from middlewares.auth import AuthMiddleware
from handlers.auth import router as auth_router
from handlers.menu import router as menu_router
from handlers.task_creation import router as task_creation_router
from handlers.calendar import router as calendar_router
from handlers.settings import router as settings_router
from services.notifications import NotificationManager

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
db = Database()

async def main():
    # Создание таблиц в базе данных
    print("Создание таблиц в базе данных...")
    await db._create_tables()
    print("Таблицы успешно созданы")
    
    # Регистрация middleware
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    
    # Регистрация роутеров
    dp.include_router(auth_router)
    dp.include_router(menu_router)
    dp.include_router(task_creation_router)
    dp.include_router(calendar_router)
    dp.include_router(settings_router)
    
    # Запуск системы уведомлений
    print("Инициализация системы уведомлений...")
    notification_manager = NotificationManager(db, bot)
    notification_task = asyncio.create_task(notification_manager.check_deadlines())
    print("Система уведомлений запущена")
    
    # Запуск бота
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен") 