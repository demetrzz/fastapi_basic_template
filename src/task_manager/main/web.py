from dishka import make_async_container, Scope
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from task_manager.main.di_provider import CoreProvider, get_async_session
from task_manager.api import root_router


def create_app() -> FastAPI:
    app = FastAPI()
    provider = CoreProvider()
    provider.provide(get_async_session, scope=Scope.REQUEST)
    container = make_async_container(provider)
    setup_dishka(container, app)
    app.include_router(root_router)
    return app
