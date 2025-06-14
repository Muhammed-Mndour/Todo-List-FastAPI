from libtodolist.data import engine_todolist
from libutil.db_session import Session


class TodolistSession(Session):

    def __init__(self, **kwargs):
        super().__init__(engine=engine_todolist, **kwargs)
