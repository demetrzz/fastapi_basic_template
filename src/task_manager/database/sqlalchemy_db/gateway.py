from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.database import models
from task_manager.database.protocols.database import DatabaseGateway
from task_manager.domain.schemas import task_schemas


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one_task(self, task: task_schemas.TaskAdd, user_id: UUID_ID):
        task = models.Task(**task.model_dump(), author_id=user_id)
        self.session.add(task)
        return task

    async def get_tasks_by_user_id(self, user_id: UUID_ID):
        result = await self.session.execute(
            select(models.Task).where(models.Task.assignee_id == user_id)
        )
        return result.scalars().all()

    async def query_task_by_id(self, task_id: int):
        result = await self.session.execute(
            select(models.Task).where(models.Task.id == task_id)
        )
        return result.scalars().first()
