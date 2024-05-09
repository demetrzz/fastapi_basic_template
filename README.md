# Fastapi-template

## Базовый шаблон для FastAPI приложения

### Стек технологий:
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest
- dishka
- fastapi-users
### Установка и настройка:

```bash
pip install -e .
```

### Настроить env:
```bash
export DB_URI=postgresql+asyncpg://user_name:testpassword@localhost/db_name
export SECRET_KEY=your_key
export ALGORITHM=your_sha_algorithm
export ACCESS_TOKEN_EXPIRES=seconds
```
### Применить миграции
```bash
alembic upgrade head
```
### Запустить:

```bash
uvicorn --factory --reload task_manager.main:create_app
```

### Тесты:

```bash
export TEST_USER_UUID=test_user_uuid
export TEST_USER_EMAIL=test_user_email
pytest
```