"""
    Модуль, в котором хранится кастомный UserManager наследованный из класса BaseUserManager.
    Который также запускает этого UserManager.
"""
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from app.auth.database import User, get_user_db
from config import JWT_SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Кастомный класс, реализующий логику Manager FastAPI_Users
    Единственное что поменял, это добавил логику по добавление (дефолту) роль id=1 (user)

    :attribute reset_password_token_secret: str - Секрет для сброса пароля:
    :attribute verification_token_secret: str - Секрет для верификации:
    """
    reset_password_token_secret = JWT_SECRET  # по хорошему это 2 отдельных секрета
    verification_token_secret = JWT_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(self, user_create: schemas.UC, safe: bool = False, request: Optional[Request] = None) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    """
    Функция для вызова Manager при создании пользователя.
    Также нужен для валидации некоторых данных, к примеру role_id, password

    :param user_db: Depends - Значение полученные из таблицы в открытой сессии:
    :return: класс UserManager:
    """
    yield UserManager(user_db)
