from typing import List

from libtodolist.messages.common import ResponseBaseModel
from libutil.util import BaseModel
from datetime import datetime, date

from .category import Category
from .priority import Priority
from .status import Status


class TaskBase(BaseModel):
    code: str | None = None
    title: str | None = None
    due_date: date | None = None


class DetailedTask(TaskBase):
    description: str | None = None
    category: str | None = None
    priority: Priority | None = None
    status: Status | None = None

    def format(self, task):
        self.code = task['task_code']
        self.title = task['title']
        self.description = task['description']
        self.category = task['category_label']
        if task['category_code'] is None:
            self.category = None
        else:
            self.category = Category(code=task['category_code'], label=task['category_label'])

        self.priority = Priority(code=task['priority_code'], label=task['priority_label'])
        self.status = Status(code=task['status_code'], label=task['status_label'])
        self.due_date = task['due_date']
        return self


class SimplifiedTask(TaskBase):
    category_code: str | None = None
    priority_code: str | None = None
    status_code: str | None = None

    def format(self, task):
        self.code = task['task_code']
        self.title = task['title']
        self.due_date = task['due_date']
        self.category_code = task['category_code']
        self.priority_code = task['priority_code']
        self.status_code = task['status_code']
        return self


class TaskDataResponse(BaseModel):
    tasks: List[SimplifiedTask] | None = []
    categories: List[Category] | None = None
    priorities: List[Priority] | None = None
    statuses: List[Status] | None = None

    def format(self, cur_tasks, categories, priorities, statuses):
        self.categories = categories
        self.priorities = priorities
        self.statuses = statuses
        self.tasks = [SimplifiedTask().format(task) for task in cur_tasks]
        return self


class GetTasksResponse(ResponseBaseModel):
    data: TaskDataResponse


class GetTaskResponse(ResponseBaseModel):
    data: DetailedTask
