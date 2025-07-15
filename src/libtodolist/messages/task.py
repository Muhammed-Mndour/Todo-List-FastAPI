from typing import List

from libtodolist.messages.common import ResponseBaseModel
from libutil.util import BaseModel
from datetime import datetime


# code
# title
# description
# priority
# due_date
# id_status
# id_category
class Task(BaseModel):
    code: str
    title: str
    description: str
    priority: int
    due_date: datetime
    id_status: int


class GetTasksResponse(ResponseBaseModel):
    data: List[Task]


class GetTaskResponse(ResponseBaseModel):
    data: Task
