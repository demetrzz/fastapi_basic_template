from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from task_manager.database.protocols.database import DatabaseGateway, UoW
from task_manager.database.sqlalchemy_db.gateway import SqlaGateway
from task_manager.main.config import load_config


async def create_async_session_maker() -> async_sessionmaker[AsyncSession]:
    config = load_config()
    engine = create_async_engine(
        config.db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "command_timeout": 5,
        },
    )
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_async_session() -> AsyncIterable[AsyncSession]:
    session_maker = await create_async_session_maker()
    async with session_maker() as session:
        yield session


class CoreProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=DatabaseGateway)
    async def new_gateway(self, session: AsyncSession) -> DatabaseGateway:
        yield SqlaGateway(session)

    @provide()
    async def new_uow(self, session: AsyncSession) -> UoW:
        return session
