"""
    Модуль, задача которого парсить секрет-данные, чтобы потом использовать их во всем проекте.
    Парсинг происходит из файла ".env".
"""
import os

from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
APP_HOST = os.getenv("APP_HOST")
APP_PORT = os.getenv("APP_PORT")
JWT_SECRET = os.getenv("JWT_SECRET")
ADMIN_CODE = os.getenv("ADMIN_CODE")
SUPERUSER_CODE = os.getenv("SUPERUSER_CODE")
