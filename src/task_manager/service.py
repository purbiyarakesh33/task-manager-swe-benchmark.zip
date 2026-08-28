from .models import Task, TaskCreate, TaskStatus, TaskUpdate, utc_now
from .repository import TaskNotFoundError, TaskRepository
from .validators import validate_title


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def create_task(self, data: TaskCreate) -> Task:
        now = utc_now()
        task = Task(
            id=self.repository.allocate_id(),
            title=validate_title(data.title),
            description=data.description,
            status=TaskStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        return self.repository.create(task)

    def get_task(self, task_id: int) -> Task:
        return self.repository.get(task_id)

    def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        return self.repository.list(status)

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        task = self.repository.get(task_id)
        task.status = TaskStatus.ACTIVE
        
        if data.title is not None:
            task.title = validate_title(data.title)
            

        if data.description is not None:
            task.description = data.description

        task.updated_at = utc_now()
        return self.repository.update(task)

    def complete_task(self, task_id: int) -> Task:
        task = self.repository.get(task_id)
        task.status = TaskStatus.COMPLETED
        task.updated_at = utc_now()
        return self.repository.update(task)

    def delete_task(self, task_id: int) -> None:
        self.repository.delete(task_id)


def build_default_service() -> TaskService:
    return TaskService(TaskRepository())
