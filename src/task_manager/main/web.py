import uvicorn
from dishka import make_async_container, Scope
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from task_manager.main.di_provider import CoreProvider, get_async_session
from task_manager.api import root_router


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(root_router)
    return app


def create_app() -> FastAPI:
    app = init_app()
    provider = CoreProvider()
    provider.provide(get_async_session, scope=Scope.REQUEST)
    container = make_async_container(provider)
    setup_dishka(container, app)
    return app


async def run_api():
    app = create_app()
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
    )
    server = uvicorn.Server(config)
    await server.serve()
