import sqlalchemy as sa
from sqlalchemy import text, types
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base

from libtodolist.data import engine_todolist
from libutil import util

Base = declarative_base()


def create_all():
    Base.metadata.create_all(engine_todolist)


def recreate_all():
    assert util.IS_DEV, 'must be dev'
    Base.metadata.drop_all(engine_todolist)
    Base.metadata.create_all(engine_todolist)


class Model(Base):
    __abstract__ = True
    __bind_key__ = 'todolist'


TINYINT = mysql.TINYINT(unsigned=True)
SMALLINT = mysql.SMALLINT(unsigned=True)
MEDIUMINT = mysql.MEDIUMINT(unsigned=True)
INT = mysql.INTEGER(unsigned=True)
BIGINT = mysql.BIGINT(unsigned=True)
SINT = mysql.INTEGER(unsigned=False)
SBIGINT = mysql.BIGINT(unsigned=False)


class User(Model):
    __tablename__ = 'user'

    id_user = sa.Column(INT, primary_key=True)
    code = sa.Column(sa.String(50), nullable=False, unique=True)

    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True)
    updated_at = sa.Column(
        types.TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        nullable=False,
        index=True,
    )


class Category(Model):
    __tablename__ = 'category'

    id_category = sa.Column(INT, primary_key=True)
    id_user = sa.Column(INT, nullable=False, index=True)
    code = sa.Column(sa.String(50), nullable=False, unique=True)
    label = sa.Column(sa.String(20), nullable=False)
    is_active = sa.Column(TINYINT, nullable=False, server_default='1', index=True)

    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True)
    updated_at = sa.Column(
        types.TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        nullable=False,
        index=True,
    )


class Task(Model):
    __tablename__ = 'task'

    id_task = sa.Column(INT, primary_key=True)
    code = sa.Column(sa.String(50), nullable=False, unique=True)
    id_user = sa.Column(INT, nullable=False, index=True)
    id_category = sa.Column(INT, nullable=True, index=True)
    title = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.String(255), nullable=True)
    id_priority = sa.Column(TINYINT, nullable=False)
    due_date = sa.Column(types.DATE, nullable=True)
    id_status = sa.Column(INT, nullable=False, index=True)
    is_active = sa.Column(TINYINT, nullable=False, server_default='1', index=True)

    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True)
    updated_at = sa.Column(
        types.TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        nullable=False,
        index=True,
    )


class Status(Model):
    __tablename__ = 'status'

    id_status = sa.Column(INT, primary_key=True)
    code = sa.Column(sa.String(10), nullable=False, unique=True)
    label = sa.Column(sa.String(15), nullable=True)

    created_at = sa.Column(types.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False, index=True)
    updated_at = sa.Column(
        types.TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
        nullable=False,
        index=True,
    )


class Priority(Model):
    __tablename__ = 'priority'

    id_priority = sa.Column(INT, primary_key=True)
    code = sa.Column(sa.String(10), nullable=False, unique=True)
    label = sa.Column(sa.String(10), nullable=True)
