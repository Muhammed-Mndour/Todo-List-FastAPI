from sqlalchemy.ext.declarative import declarative_base

from libtodolist.data import engine_todolist
from utils import util


def create_all():
    Base.metadata.create_all(engine_todolist)


def recreate_all():
    assert util.IS_DEV, 'must be dev'
    Base.metadata.drop_all(engine_todolist)
    Base.metadata.create_all(engine_todolist)


Base = declarative_base()


class Model(Base):
    __abstract__ = True
    __bind_key__ = 'todolist'
