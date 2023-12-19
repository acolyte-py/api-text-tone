# Sentiment Analysis - репозиторий проекта, который производит анализ тональности текста 🔨

Приложение состоит из множеств файлов, модулей, директорий - обо всем по порядку:

## Cтруктура проекта
```bash
.
├── alembic.ini
├── analys.log
├── app
│   ├── auth
│   │   ├── database.py
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── models.py
│   │   └── strategy.py
│   ├── __init__.py
│   ├── routers.py
│   ├── schemas.py
│   └── templates
│       ├── authorization.html
│       ├── authorized_page.html
│       ├── base.html
│       ├── purchase_failed.html
│       ├── purchase_superuser.html
│       ├── registration.html
│       └── user_profile.html
├── config.py
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 012bbd601362_init_db.py
├── ml
│   ├── config.yaml
│   ├── __init__.py
│   ├── model.py
├── poetry.lock
├── pyproject.toml
├── py-tools
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── py_tools
│   │   ├── do_lint.sh
│   │   └── __init__.py
│   └── README.md
├── README.md
├── script_db.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── test_app.py
    └── test_ml.py

10 directories, 41 files
```
### Директории
* `app/` - Директория самого приложения, включает себя файлы для основной работы приложения, его веб-сервиса в качестве клиента и сервера.
* `app/auth/` - Директория для регистрации и авторизации.
* `app/temlates/` - Директория шаблонов, страниц приложения. Там же и CSS стили и пару JS функций.
* `migrations/` - Директория инициализированная Alembic.
* `migrations/versions/` - Директория которая хранит ревизии или миграции баз данных в формате Python-модулей.
* `ml/` - Директория модели. В ней реализована логика выгрузки обученной модели и обращение к ней.
* `py-tools/` - Директория линтера, клонировал из своего репозитория для проверки кода.
* `tests/` - Директория тестов.

Отдельно также есть описание некоторым файлам:

### Файлы
* `alembic.ini` - Файл инит для работы с Alembic.
* `analys.log` - Файл лог, вывод проверки Ruff и mypy.
* `docker-compose.yml` - Конфигурационный файл проекта, который служит последним запуском, в нем поднимается 3 контейнера (app-1 = Приложение/ db-1 = База Данных/ command_runner-1 = Контейнер-зависимость, выполняет важные команды перед запуском проекта).
* `Dockerfile` - Конфигурационный файл, описывает что сделать в контейнере app-1.
* `Makefile` - Конфигурационный файл автоматизирует процессы инициализации линтера, запуск линтера и запуск тестов.
* `poetry.lock` - Автоматический файл в нём ничего руками не менять. Список зависимостей проекта.
* `pyproject.toml` - Автоматический файл. Описание проекта, необходим для дальнейшего возможного пакетирование и т. п.


## Установка 🔧
Для работы этого проекта потребуется:
- =>python3.11;
- pip;
- poetry;
- Docker;
- docker-compose;
- PostgreSQL (Если разворачивать локально);
- make (Если пользоваться Makefile);

Инструкция будет на два возможных запуска проекта:
### Запуск через `docker-compose` (Рекомендуется)
Установка Docker и docker-compose будет зависеть от ОС - предлагаю [ознакомится](https://docs.docker.com/compose/install/) с документацией и установить все необходимое.

Версии, с которыми разрабатывался проект:
```bash
    ~/soft/api-project/api-text-tone  docker --version                                                  ✔  base  
Docker version 24.0.7, build afdd53b4e3
    ~/soft/api-project/api-text-tone  docker-compose --version                                          ✔  base  
Docker Compose version v2.23.3
```

Далее необходимо клонировать проект, зайти в корневую директорию, пример:
```bash
    ~/soft/api-project/api-text-tone  pwd                                                               ✔  base  
/home/acolyte/soft/api-project/api-text-tone
```

Выполнить команду - `docker-compose up`. Если в логах не будет никаких ошибок, а в конце будет:
```bash
app-1             | INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

То сайт успешно запущен - им можно пользоваться. _О возможных ошибках, читать ниже_.

### Запуск локально
Данный способ подразумевает, что у Вас установлена `PostgerSQL` какой-нибудь аналог или `pgadmin4` для администрирования БД, можно конечно и в `psql >` оболочке.

Необходимо создать базу, запомнить её креды которые вы указывали и записать их в файл - `.env`

После необходимо клонировать проект, зайти в корневую директорию, пример:
```bash
    ~/soft/api-project/api-text-tone  pwd                                                               ✔  base  
/home/acolyte/soft/api-project/api-text-tone
```

Установить `poetry`, выполнив команду:
```bash
python3.11 -m pip install poetry | pip install poetry (Если не важно какую версию Python использовать)
```

Далее создаем виртуальное окружение:
```bash
poetry env use python3.11
```

Активируем виртуальное окружение: 
```bash
poetry shell
```

Установка пакетов для работы приложения: 
```bash
poetry install
```

После будет идти не быстрая установка, так как пакетов много. После нужно в БД, которая ранее создана сделать миграцию через Alembic:
```bash
alembic upgrade head
```

Теперь почти все готово, если при миграции проблем не было - нужно создать таблицу в базе для работы с пользователями:
```bash
python3.11 script_db.py
```

Все. Теперь можно запускать приложение:
```bash
uvicorn app.routers:app --host 0.0.0.0 --port 8080
```

Если все прошло успешно в консоли будет следующий вывод:
```bash
    ~/s/ap/api-text-tone  uvicorn app.routers:app --host 0.0.0.0 --port 8080
INFO:     Started server process [15877]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

Такой способ более усложненный чем через `Docker` - все может ещё остановится на БД, если там что-то неправильно сделать.

### Возможные проблемы/уточнения

В файле `app/auth/strategy.py` есть вот такая строчка:

```python
cookie_transport = CookieTransport(cookie_name='analysis', cookie_max_age=2592000, cookie_secure=False)
```

Куки будут отвечать за авторизированного пользователя, если её удалить из хранилища - нужно будет заново авторизоваться
Куки действуют месяц - `cookie_max_age=2592000`
Куки работают по протоколу HTTP, если в будущем использовать HTTPS - нужно будет избавиться от параметра `cookie_secure=False`

Если Вы используете способ запуска проекта через `Docker` - важная возможная проблема.
Когда Вы формируете файл `.env` то там есть некоторые значение которые возможно нужно будет поменять, пример файла:

```bash
DB_HOST=172.18.0.2
DB_PORT=5432
DB_NAME=sentiment_text
DB_USER=<>
DB_PASS=<>
APP_HOST=<>
APP_PORT=<>
JWT_SECRET=<>
ADMIN_CODE=<>
SUPERUSER_CODE=<>
```

Если Вы запустили проект, и по каким-то причинам наблюдаете, что в базу данных ничего не идёт, и по адресу `DB_HOST=172.18.0.2` БД не доступна. Нужно проверить IP адрес, командой:
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <id или name контейнера>
```

Потому что он может быть другим, если он допусти на момент проверки равен - `172.21.0.2` то в файле `.env` меняйте на `DB_HOST=172.22.0.2` и перезапускайте сервисы:

```bash
docker-compose down
#  По необходимости
    docker image prune -a
    docker builder prune -a
docker-compose up
```

Может возникнуть проблема с библиотекой `nvidia-12` _точное название не помню_

Иногда по каким-то причинам она не устанавливается. Мне помогал ребут ОС. :)

### Makefile

Краткое руководство как пользоваться `Makefile`

Установить `make`, использовалась вот такая версия:

```bash
    ~  make --version                                          ✔  base  
GNU Make 4.4.1
Эта программа собрана для x86_64-pc-linux-gnu
Copyright (C) 1988-2023 Free Software Foundation, Inc.
Лицензия GPLv3+: GNU GPL версии 3 или новее <https://gnu.org/licenses/gpl.html>
Это свободное программное обеспечение: вы можете свободно изменять его и
распространять. НЕТ НИКАКИХ ГАРАНТИЙ вне пределов, допустимых законом.
```

И далее все просто, один раз запускаем:

```bash
make setup
```

После можно пользоваться линтером, и тестами:

```bash
make lint
make test
```

## Authors 🗿

* **Миронов Миша** - *Изначальная работа* - [vk](https://vk.com/acolyte_py) | Telegramm - @acolytee.
