from jsql import sql
from libutil.sqlutil import insert_row
from libtodolist.data.models import tables


def insert_task(conn, id_user, code, title, description, id_priority, id_status, id_category):
    row = {
        'id_user': id_user,
        'code': code,
        'title': title,
        'description': description,
        'id_priority': id_priority,
        'id_status': id_status,
        'id_category': id_category,
    }
    insert_row(conn, tables.Task, row)

#
# def get_all_user_tasks(conn, id_user):
#     return sql(
#         conn,
#         '''
#         SELECT code, title, description, id_status
#         FROM task
#         WHERE id_user = :id_user
#           AND is_active = 1
#         ''',
#         id_user=id_user,
#     ).dicts()
#
#
# def get_by_code(conn, id_user, code):
#     return sql(
#         conn,
#         '''
#         SELECT code, title, description, id_status
#         FROM task
#         WHERE id_user = :id_user
#           AND code = :code
#         ''',
#         id_user=id_user,
#         code=code,
#     ).dict()
