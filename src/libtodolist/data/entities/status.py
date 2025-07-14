from jsql import sql

from libtodolist.data.models import tables


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
