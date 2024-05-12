import os
import uuid
from typing import List
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi_users.authentication import (
    JWTStrategy,
    BearerTransport,
    AuthenticationBackend,
)
from fastapi_users.schemas import BaseUser
from fastapi_users_db_sqlalchemy import UUID_ID
from starlette.testclient import TestClient

from task_manager.database.protocols.database import UoW, DatabaseGateway
from task_manager.domain.schemas.task_schemas import TaskBase
from task_manager.main import create_app
from task_manager.main.di_provider import get_async_session
from task_manager.main.fastapi_users_di import config

USER_ID = uuid.UUID(os.getenv("TEST_USER_UUID"))
USER_EMAIL = os.getenv("TEST_USER_EMAIL")


class MockCoreProvider(Provider):
    scope = Scope.APP

    @provide(provides=DatabaseGateway)
    async def new_gateway(self) -> DatabaseGateway:
        gateway = AsyncMock()
        mock_tasks: List[TaskBase] = [
            TaskBase(
                id=i,
                title=f"Task {i}",
                completed=bool(i % 2),
                author_id=USER_ID,
                assignee_id=str(uuid4()),
            )
            for i in range(5)
        ]
        gateway.get_tasks_by_user_id = AsyncMock(return_value=mock_tasks)
        yield gateway

    @provide()
    async def new_uow(self) -> UoW:
        uow = AsyncMock()
        uow.commit = AsyncMock()
        uow.flush = AsyncMock()
        return uow


@pytest_asyncio.fixture
async def container():
    provider = MockCoreProvider()
    provider.provide(get_async_session, scope=Scope.REQUEST)
    container = make_async_container(provider)
    yield container
    await container.close()


@pytest.fixture
def client(container):
    app = create_app()
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client


class MockUser(BaseUser):
    def __init__(self, id: UUID_ID, email):
        super().__init__(id=id, email=email)
        self.id = id
        self.email = email


@pytest.fixture
def test_user():
    return MockUser(USER_ID, USER_EMAIL)


@pytest.fixture
def jwt_strategy():
    return JWTStrategy(
        secret=config.jwt_secret, lifetime_seconds=config.token_expires
    )


@pytest.fixture
def auth_backend(jwt_strategy):
    bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
    return AuthenticationBackend(
        name="jwt",
        transport=bearer_transport,
        get_strategy=lambda: jwt_strategy,
    )
