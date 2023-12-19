"""
    Модуль для работы с базой данных.

    Здесь есть класс User для кастомизации определенных полей(атрибуты класса).
    Также функции, которые отвечают за парс данных и создание асинхронной сессии.
"""
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
from app.auth.models import role


DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):  # используется int, потому что наш ID: int. Можно юзать UUID
    """
    Класс для реализации логики User

    :attribute id: int - Уникальное значение пользователя:
    :attribute email: str - Электронный адрес пользователя:
    :attribute username: str - Никнейм/Имя пользователя:
    :attribute hashed_password: str - Пароль пользователя в виде хэша:
    :attribute registered_at: time - Время регистрации пользователя:
    :attribute role_id: int - Уникальное значение роли (1-user, 2-admin):
    :attribute is_active: bool - Активный пользователь или нет:
    :attribute is_superuser: bool - Супер пользователь или нет:
    :attribute is_verified: bool - Верифицирован пользователь или нет:
    """
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False)
    username: str = Column(String(length=24), nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    registered_at: TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow)
    role_id: int = Column(Integer, ForeignKey(role.c.id))
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


engine = create_async_engine(url=DB_URL)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция, которая создает асинхронную сессию

    :return AsyncGenerator: Генератор асинхронный сессии:
    """
    async with SessionLocal() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> SQLAlchemyUserDatabase:
    """
    Функция, которая получает значение таблицы User из сессии

    :param session: AsyncSession - Асинхронная сессия из функции -> get_async_session:
    :return SQLAlchemyUserDatabase: Возвращает значение из таблицы User:
    """
    yield SQLAlchemyUserDatabase(session=session, user_table=User)


async def update_user_roles(session: AsyncSession, user_id: int, new_role_id: int, is_superuser: bool) -> None:
    """
    Функция, для обновления роли (role_id) и статуса суперпользователя (is_superuser) пользователя в базе данных.

    :param session: AsyncSession - Асинхронная сессия базы данных:
    :param user_id: int - ID пользователя, которого нужно обновить:
    :param new_role_id: int - Новое значение role_id:
    :param is_superuser: bool - Новое значение is_superuser:
    """
    stmt = update(User).where(User.id == user_id).values(role_id=new_role_id, is_superuser=is_superuser)

    await session.execute(stmt)
    await session.commit()
