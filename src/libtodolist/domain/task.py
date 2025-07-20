from libtodolist.data import entities
from libutil.util import BaseModel
from datetime import datetime, date, timedelta
from pydantic import field_validator

from libtodolist.exceptions import (
    TaskValidationException,
    CategoryValidationException,
    PriorityValidationException,
    StatusValidationException,
    DueDateValidationException,
    TaskNotFoundException,
    ForbiddenActionException,
)

from src.libtodolist.data.models.tables import Priority
from src.libtodolist.exceptions import ForbiddenActionException


class AddTask(BaseModel):

    title: str
    description: str | None = None
    priority_code: str | None = None
    status_code: str | None = None
    category_code: str | None = None
    due_date: date | None = None

    @field_validator('title')
    def validate_title(cls, value: str) -> str:
        if not value:
            raise ValueError('title must not be empty')
        return value

    def execute(self, ctx, session):

        code = self._generate_task_code()
        self._initialize_fields()

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

    def _initialize_fields(self):
        if self.description is None:
            self.description = ""
        if self.priority_code is None:
            self.priority_code = "P0473"  # Medium
        if self.status_code is None:
            self.status_code = "S4589045"  # Pending
        if self.due_date is None:
            self.due_date = date.today() + timedelta(days=7)

    def _generate_task_code(self):
        return f"C{int(datetime.now().timestamp() * 1000)}"


class GetTasks(BaseModel):
    category_code: str | None = None

    def execute(self, ctx, session):
        tasks = entities.task.get_all_user_tasks(session.conn, id_user=ctx.id_user, category_code=self.category_code)
        return tasks


class GetTask(BaseModel):
    code: str

    def execute(self, ctx, session):
        task = self._validate(session.conn, ctx.id_user)
        return task

    def _validate(self, conn, id_user):
        task = entities.task.get_all_user_tasks(conn, task_code=self.code)
        if task is None:
            raise TaskNotFoundException(message=f"Task {self.code} not found")
        if task['id_user'] != id_user:
            raise ForbiddenActionException()
        return task


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
        task = entities.task.get_all_user_tasks(conn, task_code=self.code)
        if not task:
            raise TaskValidationException(f"Task {self.code} does not exist!")
        if task['id_user'] != id_user:
            raise ForbiddenActionException()

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
        task = entities.task.get_all_user_tasks(conn, task_code=code)
        if not task:
            raise TaskValidationException(f"Task {code} does not exist!")
        if task['id_user'] != id_user:
            raise ForbiddenActionException()
