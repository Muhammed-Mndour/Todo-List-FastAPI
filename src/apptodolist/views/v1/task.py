# Implement the following APIs:
# - Add Task
# - Get Tasks (the same API should support retrieving all tasks or a specific task)
# - Update Task (update any attribute of task details)
# - Delete Task

from fastapi import APIRouter, Depends
from libtodolist.context import RequestContext
from src.libtodolist.db_session import TodolistSession
from src.libtodolist.messages.common import ResponseBaseModel
from .dependencies import get_request_context
from libtodolist import domain
from libtodolist.messages.task import GetTasksResponse, GetTaskResponse

router = APIRouter()


@router.post('')
def add_task(
    msg: domain.task.AddTask,
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        msg.execute(ctx, session)
    return ResponseBaseModel(success=True, message="Task added successfully!")


# @router.get('')
# def get_tasks(
#         code: str | None = None,
#         ctx: RequestContext = Depends(get_request_context),
# ):
#     with TodolistSession() as session:
#         if code is None:
#             tasks = domain.task.GetTasks().execute(ctx, session)
#             return GetTasksResponse(success=True, data=tasks)
#         task = domain.task.GetTask().execute(ctx, session, code)
#
#     return GetTaskResponse(success=True, data=task)
