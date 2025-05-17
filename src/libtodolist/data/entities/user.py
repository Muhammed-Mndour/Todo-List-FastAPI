from jsql import sql


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
