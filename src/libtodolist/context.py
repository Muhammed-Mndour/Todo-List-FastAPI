from libtodolist.data import entities, engine_todolist
from libutil.util import BaseModel


class UserContext(BaseModel):
    id_user: int = None
    code: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_user = entities.user.get_id_by_code(engine_todolist, self.code)
