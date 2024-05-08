from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from task_manager.main.di_provider import CoreProvider
from task_manager.api import root_router


def create_app() -> FastAPI:
    app = FastAPI()
    provider = CoreProvider()
    container = make_async_container(provider)
    setup_dishka(container, app)
    app.include_router(root_router)
    return app
