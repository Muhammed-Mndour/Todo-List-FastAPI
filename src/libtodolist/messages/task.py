from typing import List

from libtodolist.messages.common import ResponseBaseModel
from libutil.util import BaseModel
from datetime import datetime, date

from .category import Category
from .priority import Priority
from .status import Status


class Task(BaseModel):
    code: str | None = None
    title: str | None = None
    description: str | None = None
    category: Category | None = None
    priority: Priority | None = None
    status: Status | None = None
    due_date: date | None = None

    def format(self, task):
        self.code = (task['task_code'],)
        self.title = (task['title'],)
        self.description = (task['description'],)
        self.category = (Category(code=task['category_code'], label=task['category_label']),)
        self.priority = (Priority(code=task['priority_code'], label=task['priority_label']),)
        self.status = (Status(code=task['status_code'], label=task['status_label']),)
        self.due_date = task['due_date']
        return self


class GetTasksResponse(ResponseBaseModel):
    data: List[Task]


class GetTaskResponse(ResponseBaseModel):
    data: Task
