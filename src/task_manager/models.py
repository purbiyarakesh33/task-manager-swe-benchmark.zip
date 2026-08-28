from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class Task(BaseModel):
    id: int
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.ACTIVE
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str = ""


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class TaskResponse(BaseModel):
    task: Task


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
