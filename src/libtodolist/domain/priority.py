from libutil.util import BaseModel
from libtodolist.data import entities


class GetPriorities(BaseModel):

    def execute(self, session):
        priorities = entities.priority.get_all_priorities(session.conn)

        return priorities
