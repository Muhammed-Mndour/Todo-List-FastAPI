from jsql import sql
from libtodolist.data.models import tables
from libutil.sqlutil import insert_row


def get_id_by_code(conn, code):
    return sql(
        conn,
        '''
        SELECT id_status
        FROM status
        WHERE code = :code
        ''',
        code=code,
    ).scalar()


def get_all_statuses(conn):
    return sql(
        conn,
        '''
        SELECT code, label
        FROM status
    ''',
    ).dicts()


def add_status(conn, code, label):
    row = {
        'code': code,
        'label': label,
    }
    insert_row(conn, tables.Status, row)
