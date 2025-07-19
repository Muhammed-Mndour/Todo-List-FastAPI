from jsql import sql

from libtodolist.data.models import tables


def get_id_by_code(conn, code):
    return sql(
        conn,
        '''
        SELECT id_priority
        FROM priority
        WHERE code = :code
        ''',
        code=code,
    ).scalar()


def get_all_priorities(conn):
    return sql(
        conn,
        '''
        SELECT code, label
        FROM priority
    ''',
    ).dicts()
