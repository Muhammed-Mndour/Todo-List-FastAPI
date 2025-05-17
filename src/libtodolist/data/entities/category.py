from libtodolist.data.models import tables
from libutil.sqlutil import insert_row


def insert_category(conn, row):
    insert_row(conn, tables.Category, row)
