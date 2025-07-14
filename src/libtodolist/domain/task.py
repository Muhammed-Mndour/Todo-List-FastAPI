from libtodolist.data import entities
from libutil.util import BaseModel
from datetime import datetime


#     code
#     title
#     description
#     priority_code
#     status_code
#     category_code
class AddTask(BaseModel):
    title: str
    description: str
    priority_code: str
    status_code: str
    category_code: str

    def execute(self, ctx, session):
        code = self._generate_task_code()
        id_priority = 1
        id_status = 1
        id_category = 1
        entities.task.insert_task(
            session.conn, ctx.id_user, code, self.title, self.description,
            id_priority, id_status, id_category
        )

    def _generate_task_code(self):
        return f"C{int(datetime.now().timestamp() * 1000)}"


class GetTasks(BaseModel):

    def execute(self, ctx, session):
        tasks = entities.task.get_all_user_tasks(session.conn, ctx.id_user)

        return tasks


class GetTask(BaseModel):
    def execute(self, ctx, session, code):
        task = entities.task.get_by_code(session.conn, ctx.id_user, code)
        return task
