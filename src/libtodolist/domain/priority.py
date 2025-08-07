from libutil.util import BaseModel
from libtodolist.data import entities
from datetime import datetime


class GetPriorities(BaseModel):

    def execute(self, session):
        priorities = entities.priority.get_all_priorities(session.conn)

        return priorities


class AddPriority(BaseModel):
    label: str

    def execute(self, session):
        code = self._generate_priority_code()
        entities.priority.add_priority(session.conn, code, self.label)

    def _generate_priority_code(self):
        return "P" + self.label[:3] + "456789"  # Keeps it 10 digits
