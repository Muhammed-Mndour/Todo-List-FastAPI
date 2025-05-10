import pytest

from utils import engines


@pytest.fixture(scope="session", autouse=True)
def engine_todolist():
    engine = engines.get_engine('todolist')
    assert engine.url.database == f'todolist'

    from repositorytodolist import models

    models.tables.create_all()

    return engine


@pytest.fixture(scope="session")
def data_todolist(engine_todolist):
    pass


@pytest.fixture(scope="session", autouse=True)
def app_todolist(data_todolist):
    from fastapi.testclient import TestClient
    from apptodolist.web import app

    return TestClient(app)
