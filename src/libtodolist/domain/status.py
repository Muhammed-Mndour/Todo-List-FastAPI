from libutil.util import BaseModel
from libtodolist.data import entities


class GetStatuses(BaseModel):

    def execute(self, session):
        statuses = entities.status.get_all_statuses(session.conn)

        return statuses
