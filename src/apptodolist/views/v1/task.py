# Implement the following APIs:
# - Add Task
# - Get Tasks (the same API should support retrieving all tasks or a specific task)
# - Update Task (update any attribute of task details)
# - Delete Task

from fastapi import APIRouter, Depends
from libtodolist.context import RequestContext
from src.libtodolist.db_session import TodolistSession
from src.libtodolist.messages.category import Category
from src.libtodolist.messages.common import ResponseBaseModel, ErrorResponse

from .dependencies import get_request_context
from libtodolist import domain

from libtodolist.messages.task import GetTasksResponse, GetTaskResponse, DetailedTask, TaskDataResponse

from typing import List


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
        tasks = msg.execute(ctx, session)
        categories: List[Category] = domain.category.GetCategories().execute(ctx, session)
        priorities: List[Priority] = domain.priority.GetPriorities().execute(session)
        statuses: List[Status] = domain.status.GetStatuses().execute(session)

    data_response: TaskDataResponse = TaskDataResponse().format(tasks, categories, priorities, statuses)
    return GetTasksResponse(success=True, data=data_response)


@router.get('/{code}')
def get_task(
    msg: domain.task.GetTask = Depends(),
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        data = msg.execute(ctx, session)

    task = DetailedTask().format(data)
    return GetTaskResponse(success=True, data=task)


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
