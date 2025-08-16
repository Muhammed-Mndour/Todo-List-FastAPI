from src.libtodolist.db_session import TodolistSession
from src.libtodolist.domain import priority as priority_table


def test_statuses():
    with TodolistSession() as session:
        priority_table.AddPriority(label="Low").execute(session)
        priority_table.AddPriority(label="Medium").execute(session)
        priority_table.AddPriority(label="High").execute(session)
