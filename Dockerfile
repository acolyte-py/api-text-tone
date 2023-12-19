FROM python:3.11

RUN pip3 install poetry

COPY pyproject.toml poetry.lock /workdir/

COPY app/ /workdir/app/
COPY ml/ /workdir/ml/

WORKDIR /workdir
RUN poetry install --no-root --no-dev

COPY . /workdir

CMD ["poetry", "run", "uvicorn", "app.routers:app", "--host", "0.0.0.0", "--port", "8080"]
