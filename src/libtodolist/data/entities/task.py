from jsql import sql
from libutil.sqlutil import insert_row
from libtodolist.data.models import tables


def insert_task(conn, id_user, code, title, description, id_priority, id_status, id_category, due_date):
    row = {
        'id_user': id_user,
        'code': code,
        'title': title,
        'description': description,
        'id_priority': id_priority,
        'id_status': id_status,
        'id_category': id_category,
        'due_date': due_date,
    }
    insert_row(conn, tables.Task, row)


def get_all_user_tasks(
    conn, id_user: str | None = None, category_code: str | None = None, task_code: str | None = None
):
    data = sql(
        conn,
        '''
        SELECT t.code     AS task_code,
               t.title    As title,
               t.description AS description,
               c.label    AS category_label,
               c.code     AS category_code,
               p.label    AS priority_label,
               p.code     AS priority_code,
               s.label    AS status_label,
               s.code     AS status_code,
               t.due_date AS due_date,
               t.id_user  AS id_user
        FROM task t
                 LEFT JOIN category c ON t.id_category = c.id_category
                 INNER JOIN priority p ON t.id_priority = p.id_priority
                 INNER JOIN status s ON t.id_status = s.id_status
        WHERE t.is_active = 1 
        {% if id_user %}
          AND t.id_user = :id_user
        {% endif %}
        {% if category_code %}
          AND c.code = :category_code
        {% endif %}
        {% if task_code %}
          AND t.code = :task_code
        {% endif %}
        ''',
        id_user=id_user,
        category_code=category_code,
        task_code=task_code,
    )
    if task_code is None:
        return data.dicts()
    return data.dict()


def update_task_by_code(conn, code, **kwargs):
    if 'title' in kwargs:
        sql(
            conn,
            '''
            UPDATE task
            SET title = :title
            WHERE code = :code
            ''',
            title=kwargs['title'],
            code=code,
        )
    if 'description' in kwargs:
        sql(
            conn,
            '''
            UPDATE task
            SET description = :description
            WHERE code = :code
            ''',
            code=code,
            description=kwargs['description'],
        )
    if 'id_category' in kwargs:
        sql(
            conn,
            '''
            UPDATE task
            SET id_category = :id_category
            WHERE code = :code
            ''',
            code=code,
            id_category=kwargs['id_category'],
        )
    if 'id_priority' in kwargs:
        sql(
            conn,
            '''
            UPDATE task
            SET id_priority = :id_priority
            WHERE code = :code
            ''',
            code=code,
            id_priority=kwargs['id_priority'],
        )
    if 'id_status' in kwargs:
        sql(
            conn,
            '''
            UPDATE task
            SET id_status = :id_status
            WHERE code = :code
            ''',
            code=code,
            id_status=kwargs['id_status'],
        )
    if 'due_date' in kwargs:
        sql(
            conn,
            '''
            UPDATE task
            SET due_date = :due_date
                WHERE code = :code
                 ''',
            code=code,
            due_date=kwargs['due_date'],
        )


def delete_task_by_code(conn, code):
    sql(
        conn,
        '''
        UPDATE task
        SET is_active = 0
        WHERE code = :code
        ''',
        code=code,
    )
