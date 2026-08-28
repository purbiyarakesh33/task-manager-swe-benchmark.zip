from fastapi.testclient import TestClient

from task_manager.api import app
from task_manager.repository import TaskRepository
from task_manager.service import TaskService
import task_manager.api as api_module


def setup_function():
    api_module.service = TaskService(TaskRepository())


client = TestClient(app)


def test_create_and_get_task():
    response = client.post(
        "/tasks",
        json={"title": "  Learn   agents ", "description": "benchmark"},
    )

    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Learn agents"

    fetched = client.get(f"/tasks/{task['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["description"] == "benchmark"


def test_missing_task_returns_404():
    response = client.get("/tasks/999")

    assert response.status_code == 404


def test_patch_only_changes_requested_fields():
    created = client.post(
        "/tasks",
        json={"title": "Original", "description": "Important"},
    ).json()

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"title": "Updated"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated"
    assert body["description"] == "Important"


def test_complete_then_filter_active():
    first = client.post("/tasks", json={"title": "Done"}).json()
    client.post(f"/tasks/{first['id']}/complete")
    client.post("/tasks", json={"title": "Still active"})

    response = client.get("/tasks?status=active")

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Still active"]


def test_delete_task():
    created = client.post("/tasks", json={"title": "Delete me"}).json()

    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204

    fetched = client.get(f"/tasks/{created['id']}")
    assert fetched.status_code == 404
