from datetime import datetime, timezone

import pytest

from task_manager.models import Task, TaskStatus
from task_manager.repository import TaskNotFoundError, TaskRepository


def make_task(task_id: int, status: TaskStatus = TaskStatus.ACTIVE) -> Task:
    now = datetime.now(timezone.utc)
    return Task(
        id=task_id,
        title=f"Task {task_id}",
        description="description",
        status=status,
        created_at=now,
        updated_at=now,
    )


def test_repository_filters_by_status():
    repo = TaskRepository()
    repo.create(make_task(1, TaskStatus.ACTIVE))
    repo.create(make_task(2, TaskStatus.COMPLETED))

    tasks = repo.list(TaskStatus.ACTIVE)

    assert [task.id for task in tasks] == [1]


def test_repository_returns_copies():
    repo = TaskRepository()
    repo.create(make_task(1))

    task = repo.get(1)
    task.title = "changed"

    assert repo.get(1).title == "Task 1"


def test_repository_raises_for_missing_task():
    repo = TaskRepository()

    with pytest.raises(TaskNotFoundError):
        repo.get(999)
