"""
    Модуль, который отвечает за хранение схем приложения.
"""
from typing import Optional
from dataclasses import dataclass

from fastapi_users import schemas
from pydantic import BaseModel


@dataclass
class SentimentPrediction:
    """
    Схема(Класс) для ответа модели в формате dataclass, используется в самой модели и тестах

    :attribute label: str - Оценка текста, в виде - (positive, neutral, negative):
    :attribute score: float - Счет точности оценки текста:
    """
    label: str
    score: float


class SentimentResponse(BaseModel):
    """
    Схема(Класс) для ответа модели в формате pydantic, используется в качестве ответа на запрос в FastAPI

    :attribute text: str - Текст, переданный в запросе для анализа:
    :attribute sentiment_label: str - Оценка текста, в виде - (positive, neutral, negative):
    :attribute sentiment_score: float - Счет точности оценки текста:
    """
    text: str
    sentiment_label: str
    sentiment_score: float


class UserRead(schemas.BaseUser[int]):
    """
    Схема(Класс) для чтение данных о пользователе

    :attribute id: int - Уникальное значение пользователя:
    :attribute username: str - Никнейм/Имя пользователя:
    :attribute email: str - Электронный адрес пользователя:
    :attribute role_id: int - Уникальное значение роли:
    :attribute is_active: bool - Активный пользователь или нет:
    :attribute is_superuser: bool - Супер пользователь или нет:
    :attribute is_verified: bool - Верифицирован пользователь или нет:
    """
    id: int
    username: str
    email: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    """
    Схема(Класс) для создание пользователя

    :attribute username: str - Никнейм/Имя пользователя:
    :attribute email: str - Электронный адрес пользователя:
    :attribute password: str - Пароль пользователя в строки (пока ещё не хэш):
    :attribute role_id: int - Уникальное значение роли:
    :attribute is_active: bool - Активный пользователь или нет:
    :attribute is_superuser: bool - Супер пользователь или нет:
    :attribute is_verified: bool - Верифицирован пользователь или нет:
    """
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
