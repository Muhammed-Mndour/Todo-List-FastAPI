from libtodolist.data import entities
from libutil.util import BaseModel


class GetTasks(BaseModel):

    def execute(self, ctx, session):
        tasks = entities.task.get_all_user_tasks(session.conn, ctx.id_user)

        return tasks
