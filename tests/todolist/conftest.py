import pytest


@pytest.fixture(scope="session", autouse=True)
def engine_todolist():
    import libtodolist

    engine = libtodolist.data.engine_todolist
    assert engine.url.database == f'todolist'

    libtodolist.data.models.tables.create_all()

    return engine


@pytest.fixture(scope="session")
def data_todolist(engine_todolist):
    pass


@pytest.fixture(scope="session", autouse=True)
def app_todolist(data_todolist):
    from fastapi.testclient import TestClient
    from apptodolist.web import app

    return TestClient(app)
