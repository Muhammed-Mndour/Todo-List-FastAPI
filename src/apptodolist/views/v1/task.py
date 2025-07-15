# Implement the following APIs:
# - Add Task
# - Get Tasks (the same API should support retrieving all tasks or a specific task)
# - Update Task (update any attribute of task details)
# - Delete Task

from fastapi import APIRouter, Depends
from libtodolist.context import RequestContext
from src.libtodolist.db_session import TodolistSession
from src.libtodolist.messages.common import ResponseBaseModel, ErrorResponse

from .dependencies import get_request_context
from libtodolist import domain

from libtodolist.messages.task import GetTasksResponse, GetTaskResponse, Task
from libtodolist.messages.category import Category
from libtodolist.messages.priority import Priority
from libtodolist.messages.status import Status


router = APIRouter()


@router.post('')
def add_task(
    msg: domain.task.AddTask,
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        msg.execute(ctx, session)
    return ResponseBaseModel(success=True, message="Task added successfully!")


@router.get('')
def get_tasks(
    msg: domain.task.GetTasks = Depends(),
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        data = msg.execute(ctx, session)

    tasks: List[Task] = []
    for task in data:
        category = Category(code=task['category_code'], label=task['category_label'])
        priority = Priority(code=task['priority_code'], label=task['priority_label'])
        status = Status(code=task['status_code'], label=task['status_label'])
        curTask = Task(
            code=task['task_code'],
            title=task['title'],
            description=task['description'],
            category=category,
            priority=priority,
            status=status,
            due_date=task['due_date'],
        )
        tasks.append(curTask)

    if not msg.code:
        return GetTasksResponse(success=True, data=tasks)

    if not data:
        return ErrorResponse(code=404, message=f"Task {msg.code} not found")

    return GetTaskResponse(success=True, data=tasks[0])


@router.put('/{code}')
def update_task(
    msg: domain.task.UpdateTask = Depends(),
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        msg.execute(ctx, session)
    return ResponseBaseModel(success=True, message="Task updated successfully!")


@router.delete('/{code}')
def delete_task(
    msg: domain.task.DeleteTask = Depends(),
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        msg.execute(ctx, session)
    return ResponseBaseModel(success=True, message="Task deleted successfully!")
