from jsql import sql


def get_all_user_tasks(conn, id_user):
    return sql(
        conn,
        '''
        SELECT code, title, description
        FROM task
        WHERE id_user = :id_user
          AND is_active = 1
        ''',
        id_user=id_user,
    ).dicts()
