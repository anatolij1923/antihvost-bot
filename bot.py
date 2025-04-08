# точка входа - запуск бота
from aiogram import Bot, Dispatcher
from handlers import start, menu
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(menu.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
