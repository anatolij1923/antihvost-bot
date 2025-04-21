# точка входа - запуск бота
from aiogram import Bot, Dispatcher
from handlers import start, menu, assignments, events
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.auth import AuthMiddleware
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.message.middleware(AuthMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(assignments.router)
    dp.include_router(events.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit") 