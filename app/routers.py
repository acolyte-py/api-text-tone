"""
    Основной модуль приложение.
    Здесь запросы как для отображения страниц, так и для основной логики запросов.
"""
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session

from ml.model import load_model
from app.schemas import SentimentResponse, UserRead, UserCreate
from app.auth.strategy import auth_backend
from app.auth.database import User, update_user_roles, get_async_session
from app.auth.manager import get_user_manager
from script_db import get_permissions_by_id
from config import SUPERUSER_CODE, ADMIN_CODE


app = FastAPI(title="Sentiment Analysis")
model = None
templates = Jinja2Templates(directory="app/templates")
fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user()
user_quotes = {}

#  Роуты для регистрации и авторизации.
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"],)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"],)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: status):
    """
    Кастомный обработчик ошибок в приложение при запросах.
    """
    if exc.status_code == 401:
        return templates.TemplateResponse("authorization.html", {"request": request})
    if exc.status_code == 403:
        return JSONResponse(content={"error": "Access denied"}, status_code=403)
    return RedirectResponse(url="/", status_code=exc.status_code)


@app.on_event("startup")
def startup_event() -> None:
    """
    Функция, при запуске приложение делает вызов модели глобальным.

    :return None:
    """
    global model
    model = load_model()


def get_user_limits(role_id: int) -> tuple:
    """

    :param role_id: int - ID роли (1, 2, 3):
    :return tuple: Возвращает кортеж со значением о количестве запросов и символов в запросе для конкретной роли:
    """
    permissions = get_permissions_by_id(role_id)
    return permissions[0], permissions[1]


def check_quotes(user_id: int, _requests: int) -> int:
    """
    Функция, которая проверяет конкретного пользователя за превышение количество запросов.
    Также каждый день - запросы обновляется, и счётчик отчитывается заново.

    :param user_id: int - ID пользователя User:
    :param _requests: int - Ограниченное количество запросов для роли:
    :return int: ID пользователя User:
    """
    if user_id not in user_quotes:
        user_quotes[user_id] = {
            "_requests_used": 0,
            "last_updated": datetime.now(),
        }

    quota = user_quotes[user_id]
    if quota["_requests_used"] >= _requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Превышен лимит запросов. Максимум {_requests} запросов разрешено в день."
        )

    if datetime.now() - quota["last_updated"] >= timedelta(days=1):
        quota["_requests_used"] = 0
        quota["last_updated"] = datetime.now()

    return user_id


async def check_limits(text: str = Form(...), current_user: User = Depends(current_active_user)):
    """
    Функция, которая проверяет конкретного пользователя за превышение количество символов в запросе.

    :param text: str - Текст полученный из введенной в форму на вебе:
    :param current_user: User(Depends) - Зависимость от авторизованного пользователя:
    :return str: Возвращает текст:
    """
    role_id = current_user.role_id
    _req, _sym = get_user_limits(role_id)

    if len(text) > _sym:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Превышен лимит символов. Максимум {_sym} символов разрешено."
        )

    check_quotes(current_user.id, _req)

    return text


@app.post("/predict", tags=["app"],)
async def predict_sentiment(
        text: str = Depends(check_limits), current_user: User = Depends(current_active_user)) -> SentimentResponse:
    """
    Главный запрос приложения, который отправляет на форму текст - анализируется и выдает ответ.

    :param text: Depends(check_limits) Зависимость от текста проверенного в функции check_limits:
    :param current_user: User(Depends) - Зависимость от авторизованного пользователя:
    :return SentimentResponse: Возвращает ответ в виде схемы SentimentResponse:
    """

    sentiment = model(text)
    response = SentimentResponse(text=text, sentiment_label=sentiment.label, sentiment_score=sentiment.score)
    user_quotes[current_user.id]["_requests_used"] += 1
    return response


@app.get("/", response_class=HTMLResponse, tags=["app"])
async def show_result(request: Request, current_user: User = Depends(current_active_user)):
    """
    Главная(Корневая "/") страница приложения.

    :param request: Request - обязательный аргумент при работе с FastAPI(HTML):
    :param current_user: User(Depends) - Зависимость от авторизованного пользователя:
    :return TemplateResponse: Отображает страницу в HTML формате:
    """
    username = current_user.username
    context = {
        "request": request,
        "current_user": current_user,
        "username": username,
    }
    return templates.TemplateResponse("authorized_page.html", context)


@app.get("/reg", response_class=HTMLResponse, tags=["app"],)
async def registration(request: Request):
    """
    Функция для отображения страницы "Регистрация"

    :param request: Request - обязательный аргумент при работе с FastAPI(HTML):
    :return TemplateResponse: Отображает страницу в HTML формате:
    """
    return templates.TemplateResponse("registration.html", {"request": request})


@app.get("/login", response_class=HTMLResponse, tags=["app"],)
async def authorization(request: Request):
    """
    Функция для отображения страницы "Авторизация"

    :param request: Request - обязательный аргумент при работе с FastAPI(HTML):
    :return TemplateResponse: Отображает страницу в HTML формате:
    """
    return templates.TemplateResponse("authorization.html", {"request": request})


@app.get("/profile", response_class=HTMLResponse, tags=["user"],)
async def user_profile(request: Request, current_user: User = Depends(current_active_user)):
    """
    Функция для отображения страницы "Профиль пользователя"

    :param request: Request - обязательный аргумент при работе с FastAPI(HTML):
    :param current_user: User(Depends) - Зависимость от авторизованного пользователя:
    :return TemplateResponse: Отображает страницу в HTML формате:
    """
    username = current_user.username
    email = current_user.email
    role_id = current_user.role_id
    _requests = get_permissions_by_id(int(role_id))[0]
    _symbols = get_permissions_by_id(int(role_id))[1]
    _role_name = get_permissions_by_id(int(role_id))[2]

    context = {
        "request": request,
        "username": username,
        "email": email,
        "_requests": _requests,
        "_symbols": _symbols,
        "_role_name": _role_name,
        "current_user": current_user,
    }
    return templates.TemplateResponse("user_profile.html", context)


@app.get("/purchase", response_class=HTMLResponse, tags=["user"],)
async def purchase_superuser(request: Request, current_user: User = Depends(current_active_user)):
    """
    Функция для отображения страницы "Покупка супер-пользователя"

    :param request: Request - обязательный аргумент при работе с FastAPI(HTML):
    :param current_user: User(Depends) - Зависимость от авторизованного пользователя:
    :return TemplateResponse: Отображает страницу в HTML формате, либо RedirectResponse, если ты уже супер-пользователь:
    """
    if current_user.is_superuser:
        return RedirectResponse(url="/profile", status_code=303)

    username = current_user.username
    context = {
        "request": request,
        "current_user": current_user,
        "username": username
    }
    return templates.TemplateResponse("purchase_superuser.html", context)


@app.get("/purchase_failed", response_class=HTMLResponse, tags=["user"],)
async def authorization(request: Request, current_user: User = Depends(current_active_user)):
    """
    Функция для отображения страницы "Неуспешная покупка"

    :param request: Request - обязательный аргумент при работе с FastAPI(HTML):
    :param current_user: User(Depends) - Зависимость от авторизованного пользователя:
    :return TemplateResponse: Отображает страницу в HTML формате:
    """
    username = current_user.username
    return templates.TemplateResponse("purchase_failed.html", {"request": request, "username": username})


@app.post("/purchase", response_class=HTMLResponse, tags=["user"])
async def handle_purchase(
        code: str = Form(...),
        current_user: User = Depends(current_active_user),
        db: Session = Depends(get_async_session)
):
    """
    Функция для обработки покупки супер-пользователя, при вводе кода с нужной логикой.

    :param code: str - Код, который "покупается" для повышения прав пользователей:
    :param current_user: User(Depends) - Зависимость от авторизованного пользователя:
    :param db: Session(get_async_session) - Асинхронная сессия к базе данных:
    :return RedirectResponse: После валидации кода, идёт редирект в зависимости от введенного кода (Правильный или Нет):
    """
    ROLES_MAPPING = {
        SUPERUSER_CODE: {"role_id": 2, "is_superuser": True},
        ADMIN_CODE: {"role_id": 3, "is_superuser": False}
    }
    if code in ROLES_MAPPING:
        role_info = ROLES_MAPPING[code]
        await update_user_roles(
            db,
            user_id=current_user.id,
            new_role_id=role_info["role_id"],
            is_superuser=role_info["is_superuser"],
        )
        return RedirectResponse(url="/profile", status_code=303)
    else:
        return RedirectResponse(url="/purchase_failed", status_code=303)
