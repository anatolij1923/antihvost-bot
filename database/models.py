from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, Text
from datetime import datetime
from typing import Optional
import os

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Модель студента
class Student(Base):
    __tablename__ = "students"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    group_name: Mapped[str] = mapped_column(String(50))
    is_authorized: Mapped[bool] = mapped_column(Boolean, default=False)

# Модель лабораторной работы
class LabWork(Base):
    __tablename__ = "lab_works"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    max_score: Mapped[int] = mapped_column(Integer)

# Модель сдачи лабораторной работы
class LabSubmission(Base):
    __tablename__ = "lab_submissions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.user_id"))
    lab_id: Mapped[int] = mapped_column(ForeignKey("lab_works.id"))
    submission_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20))  # submitted, checked, returned

class Database:
    def __init__(self, db_url: str = "sqlite+aiosqlite:///database/bot.db"):
        self.engine = create_async_engine(db_url, echo=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def _create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Методы для работы со студентами
    async def add_student(self, user_id: int, full_name: str, group_name: str):
        async with self.async_session() as session:
            student = Student(
                user_id=user_id,
                full_name=full_name,
                group_name=group_name,
                is_authorized=True
            )
            session.add(student)
            await session.commit()

    async def get_student(self, user_id: int) -> Optional[Student]:
        async with self.async_session() as session:
            return await session.get(Student, user_id)

    async def is_authorized(self, user_id: int) -> bool:
        student = await self.get_student(user_id)
        return student is not None and student.is_authorized

    # Методы для работы с лабораторными работами
    async def add_lab_work(self, title: str, description: str, deadline: datetime, max_score: int):
        async with self.async_session() as session:
            lab = LabWork(
                title=title,
                description=description,
                deadline=deadline,
                max_score=max_score
            )
            session.add(lab)
            await session.commit()
            return lab

    async def get_lab_work(self, lab_id: int) -> Optional[LabWork]:
        async with self.async_session() as session:
            return await session.get(LabWork, lab_id)

    # Методы для работы с сдачами лабораторных работ
    async def submit_lab_work(self, student_id: int, lab_id: int):
        async with self.async_session() as session:
            submission = LabSubmission(
                student_id=student_id,
                lab_id=lab_id,
                status="submitted"
            )
            session.add(submission)
            await session.commit()
            return submission

    async def get_student_submissions(self, student_id: int):
        async with self.async_session() as session:
            return await session.query(LabSubmission).filter(
                LabSubmission.student_id == student_id
            ).all()

    async def close(self):
        async with self.async_session() as session:
            await session.close() 