from fastapi_users_db_sqlalchemy import UUID_ID
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    author_id: UUID_ID
    assignee_id: UUID_ID


class TaskAdd(BaseModel):
    title: str
    assignee_id: UUID_ID


class TaskCompletion(BaseModel):
    completed: bool
