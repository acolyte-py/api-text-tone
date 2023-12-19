"""
    Модуль в котором реализована логика стратегии auth_backend: JWT + cookie
    cookie_secure=False - Необходимо для создание куки на протоколе HTTP. Если сделать сертификат - параметр не нужен
"""
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from config import JWT_SECRET


cookie_transport = CookieTransport(cookie_name='analysis', cookie_max_age=2592000, cookie_secure=False)  # 30 days


def get_jwt_strategy() -> JWTStrategy:
    """
    Функция, реализующая стратегию через: JWT + cookie

    :return: класс JWTStrategy
    """
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
