from typing import List

from libtodolist.messages.common import ResponseBaseModel
from libutil.util import BaseModel
from datetime import datetime, date


class Task(BaseModel):
    code: str
    title: str
    description: str | None = None
    id_category: int
    id_priority: int
    id_status: int
    due_date: date


class GetTasksResponse(ResponseBaseModel):
    data: List[Task]


class GetTaskResponse(ResponseBaseModel):
    data: Task
