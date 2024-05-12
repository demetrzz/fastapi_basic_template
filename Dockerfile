FROM python:3.12.3-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apk update && apk add python3-dev gcc libc-dev
RUN pip3 install --upgrade pip setuptools
RUN pip install poetry

WORKDIR /app/src
COPY pyproject.toml  poetry.lock ./
RUN poetry install

COPY ./src /app/src

CMD ["python", "-Om", "task_manager"]