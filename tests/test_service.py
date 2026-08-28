from task_manager.models import TaskCreate, TaskStatus, TaskUpdate
from task_manager.repository import TaskRepository
from task_manager.service import TaskService


def make_service() -> TaskService:
    return TaskService(TaskRepository())


def test_create_task_assigns_id_and_active_status():
    service = make_service()

    task = service.create_task(TaskCreate(title="  Ship   feature "))

    assert task.id == 1
    assert task.title == "Ship feature"
    assert task.status == TaskStatus.ACTIVE


def test_update_is_partial_and_preserves_other_fields():
    service = make_service()
    original = service.create_task(
        TaskCreate(title="Original", description="Keep this")
    )

    updated = service.update_task(
        original.id,
        TaskUpdate(title="New title"),
    )

    assert updated.title == "New title"
    assert updated.description == "Keep this"
    assert updated.status == TaskStatus.ACTIVE


def test_complete_task_changes_only_status_and_timestamp():
    service = make_service()
    task = service.create_task(TaskCreate(title="Finish me"))

    completed = service.complete_task(task.id)

    assert completed.title == "Finish me"
    assert completed.status == TaskStatus.COMPLETED
    assert completed.updated_at >= task.updated_at


def test_list_can_filter_status():
    service = make_service()
    first = service.create_task(TaskCreate(title="first"))
    service.complete_task(first.id)
    service.create_task(TaskCreate(title="second"))

    active = service.list_tasks(TaskStatus.ACTIVE)

    assert [task.title for task in active] == ["second"]
