FROM python:3.12.3-alpine
RUN apk update && apk add python3-dev gcc libc-dev
RUN pip3 install --upgrade pip setuptools
RUN pip install gunicorn

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./src /app/src
COPY ./pyproject.toml ./

RUN pip install .

CMD ["uvicorn", "--factory", "--reload", "--host", "0.0.0.0", "--port", "8000", "task_manager.main:create_app"]