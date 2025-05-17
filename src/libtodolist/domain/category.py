import time

from pydantic import field_validator

from libtodolist.data import entities
from libutil.util import BaseModel


class AddCategory(BaseModel):
    label: str

    @field_validator('label')
    @classmethod
    def validate_label(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError('label must be alphanumeric')
        return value

    def execute(self, user_context, session):
        category = {
            'code': f'C{int(time.time())}T',
            'label': self.label,
        }

        entities.category.insert_category(session.conn, category)
