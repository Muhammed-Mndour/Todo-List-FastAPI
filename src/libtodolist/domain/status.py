from libutil.util import BaseModel
from libtodolist.data import entities
from datetime import datetime


class GetStatuses(BaseModel):

    def execute(self, session):
        statuses = entities.status.get_all_statuses(session.conn)

        return statuses


class AddStatus(BaseModel):
    label: str

    def execute(self, session):
        code = self._generate_status_code()
        entities.status.add_status(session.conn, code, self.label)

    def _generate_status_code(self):
        return "S" + self.label[:3] + "456789"  # Keeps it 10 digits
