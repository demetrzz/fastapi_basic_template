from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request

from task_manager.database.protocols.database import DatabaseGateway, UoW
from task_manager.main.celery_worker import create_task

index_router = APIRouter(route_class=DishkaRoute)


@index_router.get("/{n}")
async def index(
    request: Request,
    database: FromDishka[DatabaseGateway],
    uow: FromDishka[UoW],
    n: int,
) -> dict:
    create_task.delay(n)  # celery background task
    return {}
