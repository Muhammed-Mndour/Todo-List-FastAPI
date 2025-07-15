from typing import List

from libtodolist.messages.common import ResponseBaseModel
from libutil.util import BaseModel
from datetime import datetime, date

from .category import Category
from .priority import Priority
from .status import Status


class Task(BaseModel):
    code: str
    title: str
    description: str | None = None
    category: Category
    priority: Priority
    status: Status
    due_date: date


class GetTasksResponse(ResponseBaseModel):
    data: List[Task]


class GetTaskResponse(ResponseBaseModel):
    data: Task
