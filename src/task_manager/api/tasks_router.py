from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Depends

from task_manager.domain.models import User
from task_manager.domain.schemas.task_schemas import (
    TaskAdd,
    TaskCompletion,
    TaskBase,
)
from task_manager.domain.services.tasks_services import (
    add_one_task,
    get_users_tasks,
    update_task,
    InvalidTask,
    NoPermission,
)
from task_manager.main.fastapi_users_di import current_active_user
from task_manager.adapters.protocols.database import DatabaseGateway, UoW

tasks_router = APIRouter(route_class=DishkaRoute)


@tasks_router.get("")
async def get_tasks(
    database: FromDishka[DatabaseGateway],
    current_user: User = Depends(current_active_user),
) -> list:
    try:
        tasks = await get_users_tasks(database, current_user.id)
    except InvalidTask:
        raise HTTPException(
            status_code=404, detail="This user doesnt have any tasks"
        )
    return tasks


@tasks_router.post("")
async def add_task(
    database: FromDishka[DatabaseGateway],
    uow: FromDishka[UoW],
    task: TaskAdd,
    current_user: User = Depends(current_active_user),
) -> TaskBase:
    return await add_one_task(database, uow, task, current_user.id)


@tasks_router.patch("/{id}")
async def edit_task_completion(
    database: FromDishka[DatabaseGateway],
    uow: FromDishka[UoW],
    id: int,
    task: TaskCompletion,
    current_user: User = Depends(current_active_user)
) -> TaskBase:
    try:
        task = await update_task(database, uow, current_user.id, id, task)
    except InvalidTask:
        raise HTTPException(status_code=404, detail="Task not found")
    except NoPermission:
        raise HTTPException(
            status_code=400,
            detail="You are not author or assignee of this task",
        )
    return task
