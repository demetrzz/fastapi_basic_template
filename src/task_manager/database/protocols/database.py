from abc import ABC, abstractmethod
from typing import Protocol

from fastapi_users_db_sqlalchemy import UUID_ID


class UoW(Protocol):
    async def commit(self):
        pass

    async def flush(self):
        pass


class DatabaseGateway(ABC):
    @abstractmethod
    async def add_one_task(self, task, user_id: UUID_ID):
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_by_user_id(self, user_id):
        raise NotImplementedError

    @abstractmethod
    async def query_task_by_id(self, task_id):
        raise NotImplementedError
