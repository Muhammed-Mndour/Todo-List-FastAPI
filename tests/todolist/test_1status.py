from src.libtodolist.db_session import TodolistSession
from src.libtodolist.domain import status as status_table


def test_statuses():
    with TodolistSession() as session:
        status_table.AddStatus(label="New").execute(session)
        status_table.AddStatus(label="In Progress").execute(session)
        status_table.AddStatus(label="Completed").execute(session)
        status_table.AddStatus(label="Canceled").execute(session)
