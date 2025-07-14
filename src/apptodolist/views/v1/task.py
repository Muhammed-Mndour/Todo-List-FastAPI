# Implement the following APIs:
# - Add Task
# - Get Tasks (the same API should support retrieving all tasks or a specific task)
# - Update Task (update any attribute of task details)
# - Delete Task
from fastapi import APIRouter, Depends
from libtodolist.context import RequestContext
from src.libtodolist.db_session import TodolistSession
from .dependencies import get_request_context
from libtodolist import domain

router = APIRouter()


@router.get('')
def get_tasks(
        ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        tasks = domain.task.GetTasks().execute(ctx, session)
    return tasks
