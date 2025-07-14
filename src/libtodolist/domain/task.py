from libtodolist.data import entities
from libutil.util import BaseModel
from datetime import datetime
from pydantic import field_validator

class AddTask(BaseModel):
    title: str
    description: str
    priority_code: str | None = "High"
    status_code: str | None = "Pending"
    category_code: str | None = "C1752504942590"

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

        print("funnn ", id_status)
        entities.task.insert_task(
            session.conn, ctx.id_user, code, self.title, self.description,
            id_priority, id_status, id_category
        )

    def _generate_task_code(self):
        return f"C{int(datetime.now().timestamp() * 1000)}"



#
# class GetTasks(BaseModel):
#
#     def execute(self, ctx, session):
#         tasks = entities.task.get_all_user_tasks(session.conn, ctx.id_user)
#
#         return tasks
#
#
# class GetTask(BaseModel):
#     def execute(self, ctx, session, code):
#         task = entities.task.get_by_code(session.conn, ctx.id_user, code)
#         return task
