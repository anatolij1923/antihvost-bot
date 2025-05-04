from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import asyncio
import os
from dotenv import load_dotenv
from database import Database
from middlewares.auth import AuthMiddleware
from handlers.auth import router as auth_router

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
db = Database()

async def main():
    # Создание таблиц в базе данных
    await db._create_tables()
    
    # Регистрация middleware
    dp.message.middleware(AuthMiddleware())
    
    # Регистрация роутеров
    dp.include_router(auth_router)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен") 