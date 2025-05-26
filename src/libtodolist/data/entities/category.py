from jsql import sql

from libtodolist.data.models import tables
from libutil.sqlutil import insert_row


def insert_category(conn, id_user, code, label):
    row = {
        'id_user': id_user,
        'code': code,
        'label': label,
    }

    insert_row(conn, tables.Category, row)


def get_categories(conn, id_user):
    return sql(
        conn,
        '''
        SELECT code, label
        FROM category
        WHERE id_user = :id_user
          AND is_active = 1
    ''',
        id_user=id_user,
    ).dicts()


# TODO: cache this
def get_id_by_code(conn, code, is_active=False):
    return sql(
        conn,
        '''
        SELECT id_category
        FROM category
        WHERE code = :code
        {% if is_active %}
          AND is_active = :is_active
        {% endif %}
    ''',
        code=code,
        is_active=is_active,
    ).scalar()


def get_by_code(conn, code, is_active=False):
    return sql(
        conn,
        '''
        SELECT id_category, id_user, code, label
        FROM category
        WHERE code = :code
        {% if is_active %}
          AND is_active = :is_active
        {% endif %}
    ''',
        code=code,
        is_active=is_active,
    ).dict()


# TODO: add update in sqlutil
def update_category(conn, code, label):
    sql(
        conn,
        '''
        UPDATE category
        SET label = :label
        WHERE code = :code
        ''',
        code=code,
        label=label,
    )


def delete_category(conn, code):
    sql(
        conn,
        '''
        UPDATE category
        SET is_active = 0
        WHERE code = :code
        ''',
        code=code,
    )
