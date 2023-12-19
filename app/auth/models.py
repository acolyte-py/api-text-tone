"""
    Модуль, для будущих таблиц в базе данных. DB: "PostgreSQL"
    Тут используется MetaData решение, сам же больше отдаю предпочтение `declarative_base`
    Считаю что такой подход более правильным чем MetaData, его проще воспринимать и легче с ним работается.
"""
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, JSON, ForeignKey, Boolean

from datetime import datetime


metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String(length=24), nullable=False),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)
