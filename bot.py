from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import asyncio
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    # Регистрация middleware
    # dp.message.middleware(AuthMiddleware())
    
    # Регистрация роутеров
    # dp.include_router(start.router)
    # dp.include_router(menu.router)
    # dp.include_router(assignments.router)
    # dp.include_router(events.router)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен") 