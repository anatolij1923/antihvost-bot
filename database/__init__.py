from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Создание асинхронного движка базы данных
engine = create_async_engine(
    os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db"),
    echo=True
)

# Создание фабрики сессий
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """Получение сессии базы данных"""
    async with async_session() as session:
        yield session

__all__ = ['engine', 'async_session', 'get_session'] 