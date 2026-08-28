from copy import deepcopy

from .models import Task, TaskStatus


class TaskNotFoundError(Exception):
    pass


class TaskRepository:
    """In-memory persistence layer.

    The API/service layer should not know how tasks are stored.
    """

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create(self, task: Task) -> Task:
        self._tasks[task.id] = deepcopy(task)
        self._next_id = max(self._next_id, task.id + 1)
        return deepcopy(task)

    def allocate_id(self) -> int:
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def get(self, task_id: int) -> Task:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"task {task_id} not found")
        return deepcopy(task)

    def list(self, status: TaskStatus | None = None) -> list[Task]:
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [task for task in tasks if task.status == status]
        tasks.sort(key=lambda task: task.id)
        return deepcopy(tasks)

    def update(self, task: Task) -> Task:
        if task.id not in self._tasks:
            raise TaskNotFoundError(f"task {task.id} not found")
        self._tasks[task.id] = deepcopy(task)
        return deepcopy(task)

    def delete(self, task_id: int) -> None:
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"task {task_id} not found")
        del self._tasks[task_id]
