from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import Student, Base
from .database import Database

load_dotenv()

# Создаем директорию для базы данных, если её нет
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)

engine = create_async_engine(
    os.getenv("DATABASE_URL", "sqlite+aiosqlite:///database/bot.db"),
    echo=True
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """Получение сессии базы данных"""
    async with async_session() as session:
        yield session

__all__ = ['engine', 'async_session', 'get_session', 'Database', 'Student', 'Base'] 