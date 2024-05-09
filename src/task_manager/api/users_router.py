from fastapi import APIRouter

from task_manager.domain.schemas.user_schemas import (
    UserRead,
    UserUpdate,
    UserCreate,
)
from task_manager.main.fastapi_users_di import (
    fastapi_users,
    auth_backend,
)

users_router = APIRouter()


users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
)
users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)
users_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
)
users_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
)
users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)
