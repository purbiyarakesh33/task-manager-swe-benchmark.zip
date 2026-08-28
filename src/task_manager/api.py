from fastapi import FastAPI, HTTPException, Query

from .models import Task, TaskCreate, TaskStatus, TaskUpdate
from .repository import TaskNotFoundError
from .service import TaskService, build_default_service

app = FastAPI(title="Task Manager API", version="0.1.0")
service: TaskService = build_default_service()


def _not_found(exc: TaskNotFoundError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(exc))


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate) -> Task:
    try:
        return service.create_task(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    status: TaskStatus | None = Query(default=None),
) -> list[Task]:
    return service.list_tasks(status)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as exc:
        raise _not_found(exc)


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate) -> Task:
    try:
        return service.update_task(task_id, data)
    except (TaskNotFoundError, ValueError) as exc:
        if isinstance(exc, TaskNotFoundError):
            raise _not_found(exc)
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int) -> Task:
    try:
        return service.complete_task(task_id)
    except TaskNotFoundError as exc:
        raise _not_found(exc)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    try:
        service.delete_task(task_id)
    except TaskNotFoundError as exc:
        raise _not_found(exc)
