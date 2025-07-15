from libtodolist.data import entities
from libutil.util import BaseModel
from datetime import datetime, date, timedelta
from pydantic import field_validator
from fastapi import HTTPException, Body
from libtodolist.exceptions import (
    TaskValidationException,
    CategoryValidationException,
    PriorityValidationException,
    StatusValidationException,
    DueDateValidationException,
)

from src.libtodolist.data.models.tables import Priority


class AddTask(BaseModel):

    title: str
    description: str = ""
    priority_code: str = "P0473"  # Medium
    status_code: str = "S4589045"  # Pending
    category_code: str = "C1752577374150"  # None
    due_date: date = date.today() + timedelta(days=7)

    @field_validator('title')
    def validate_label(cls, value: str) -> str:
        if not value:
            raise ValueError('title must not be empty')
        return value

    def execute(self, ctx, session):
        code = self._generate_task_code()
        id_priority = entities.priority.get_id_by_code(session.conn, self.priority_code)
        id_status = entities.status.get_id_by_code(session.conn, self.status_code)
        id_category = entities.category.get_id_by_code(session.conn, self.category_code)

        entities.task.insert_task(
            session.conn,
            ctx.id_user,
            code,
            self.title,
            self.description,
            id_priority,
            id_status,
            id_category,
            self.due_date,
        )

    def _generate_task_code(self):
        return f"C{int(datetime.now().timestamp() * 1000)}"


class GetTasks(BaseModel):
    code: str | None = None

    def execute(self, ctx, session):
        if not self.code:
            tasks = entities.task.get_all_user_tasks(session.conn, ctx.id_user)
            return tasks
        else:
            task = entities.task.get_by_code(session.conn, ctx.id_user, self.code)
            return task


# {
#   "title": "task2",
#   "description": "task2 description",
#   "id_category: "C1752504942590",
#   "id_priority": "P2438",
#   "id_status": "S4589045",
#   "due_date": "2025-07-14"
# }
class UpdateTask(BaseModel):
    class Task(BaseModel):
        title: str | None = None
        description: str | None = None
        category_code: str | None = None
        priority_code: str | None = None
        status_code: str | None = None
        due_date: date | None = None

    code: str
    task: Task

    def execute(self, ctx, session):
        kwargs = {}
        self._validate(
            session.conn,
            ctx.id_user,
            self.task.title,
            self.task.description,
            self.task.category_code,
            self.task.priority_code,
            self.task.status_code,
            self.task.due_date,
            kwargs,
        )
        entities.task.update_task_by_code(session.conn, self.code, **kwargs)

    def _validate(self, conn, id_user, title, description, category_code, priority_code, status_code, due_date, kwargs):
        task = entities.task.get_by_code(conn, id_user, self.code)
        if not task:
            raise TaskValidationException(f"Task {self.code} does not exist!")

        if title:
            kwargs['title'] = title

        if description:
            kwargs['description'] = description

        if category_code:
            id_category = entities.category.get_id_by_code(conn, category_code)
            if not id_category:
                raise CategoryValidationException(f"Category {category_code} does not exist!")
            kwargs['id_category'] = id_category

        if priority_code:
            id_priority = entities.priority.get_id_by_code(conn, priority_code)
            if not id_priority:
                raise PriorityValidationException(f"Priority {priority_code} does not exist!")
            kwargs['id_priority'] = id_priority

        if status_code:
            id_status = entities.status.get_id_by_code(conn, status_code)
            if not id_status:
                raise StatusValidationException(f"Status {status_code} does not exist!")
            kwargs['id_status'] = id_status

        if due_date:
            if due_date < date.today():
                raise DueDateValidationException(f"Due date {due_date} must be in the future!")
            kwargs['due_date'] = due_date


class DeleteTask(BaseModel):
    code: str

    def execute(self, ctx, session):
        self._validate(session.conn, ctx.id_user, self.code)
        entities.task.delete_task_by_code(session.conn, self.code)

    def _validate(self, conn, id_user, code):
        task = entities.task.get_by_code(conn, id_user, code)
        if not task:
            raise TaskValidationException(f"Task {code} does not exist!")
