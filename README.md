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
- docker

### Запуск:
Создать .env и заполнить используя пример
```bash
docker compose build
docker compose up
```
### Тесты:

```bash
export TEST_USER_UUID=test_user_uuid
export TEST_USER_EMAIL=test_user_email
pytest
```