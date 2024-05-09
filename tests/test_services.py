import pytest

from task_manager.database.protocols.database import DatabaseGateway
from task_manager.domain.schemas.task_schemas import TaskBase
from task_manager.domain.services.tasks_services import get_users_tasks


@pytest.mark.asyncio
async def test_get_users_tasks(container, test_user):
    database = await container.get(DatabaseGateway)

    tasks = await get_users_tasks(database, test_user.id)

    for task in tasks:
        assert isinstance(task, TaskBase)
        assert task.author_id == test_user.id
