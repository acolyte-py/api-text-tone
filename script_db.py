"""
    Специальный модуль для начало работы всего сайта.
    Здесь активные функции, которые используются для инициализации БД.
"""
from sqlalchemy import create_engine, MetaData, insert, select
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
from app.auth.models import role


DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DB_URL)
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def populate_users_table() -> None:
    """
    Функция, для заполнения таблицы "role".
    Необходимая функция, чтобы задать права будущим пользователям.

    :return None: Ничего не возвращает, делает коммит в базу и все:
    """
    db_data = [
        {"id": "1", "name": "user", "permissions": {"_requests": 50, "_symbols": 100}},
        {"id": "2", "name": "superuser", "permissions": {"_requests": 500, "_symbols": 250}},
        {"id": "3", "name": "admin", "permissions": {"_requests": 99999, "_symbols": 99999}},
    ]

    for item in db_data:
        db.execute(insert(role).values(**item))

    db.commit()


def view_role_table() -> dict:
    """
    Функция, для получения данных из таблицы "role", в кастомном словаре.

    :return dict: Возвращает словарь с данными из таблицы "role":
    """
    query = select(role)
    result = db.execute(query)

    column_names = result.keys()
    role_data = {"role_data": [dict(zip(column_names, row)) for row in result]}

    return role_data


def get_permissions_by_id(role_id: int) -> tuple:
    """
    Функция, для отображения прав конкретной роли из таблицы "role".

    :param role_id: int - ID роли (1, 2, 3):
    :return tuple: Возвращает кортеж в формате - int, int, str):
    """
    data: dict = view_role_table()
    for _role in data["role_data"]:
        if _role["id"] == role_id:
            return _role["permissions"]["_requests"], _role["permissions"]["_symbols"], _role["name"]


if __name__ == "__main__":
    populate_users_table()
