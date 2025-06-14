from jsql import sql

from libtodolist.data.models import tables
from libutil.sqlutil import insert_row


def get_id_by_code(conn, code):
    return sql(
        conn,
        '''
        SELECT id_user
        FROM user
        WHERE code = :code
    ''',
        code=code,
    ).scalar()


def insert_user(conn, code):
    id_user = insert_row(conn, tables.User, {'code': code}).lastrowid
    return id_user
