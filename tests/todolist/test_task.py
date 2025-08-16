import random
from src.libtodolist.db_session import TodolistSession
from src.libtodolist.data.entities import task as TaskTable
from src.libtodolist.data.entities import priority as priority_table
from src.libtodolist.data.entities import status as status_table
from src.libtodolist.domain.enums.priority import  PriorityLabel
from src.libtodolist.domain.enums.status import StatusLabel


from http import HTTPStatus

X_User_Code = "mhmd"
headers = {"X-User-Code": X_User_Code}
invalid_task_code = "fffffffff"
# -----------------------------
# Create Task
# -----------------------------


def test_post_task_creates_and_returns_ok(app_todolist):
    with TodolistSession() as session:
        status_code = status_table.get_code_by_label(session.conn,StatusLabel.NEW)
        priority_code = priority_table.get_code_by_label(session.conn,PriorityLabel.MEDIUM)
        payload = {
            "title": "Home work",
            "description": "Home work description",
            "priority_code": priority_code,
            "status_code": status_code,
            "due_date": "2030-09-23",
        }
    res = app_todolist.post("/v1/tasks", headers=headers, json=payload)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"success": True, "code": HTTPStatus.OK, "message": "Task added successfully!", "data": {}}


def test_post_task_rejects_empty_title_with_bad_request(app_todolist):
    payload = {"title": ""}
    res = app_todolist.post("/v1/tasks", headers=headers, json=payload)
    assert res.status_code == HTTPStatus.BAD_REQUEST
    body = res.json()
    assert body["success"] is False
    parsed_message = eval(body["message"])
    assert parsed_message[0]['msg'] == "Value error, title must not be empty"


# -----------------------------
# Get Tasks
# -----------------------------


def test_get_tasks_returns_ok_and_list(app_todolist):
    with TodolistSession() as session:
        status_code = status_table.get_code_by_label(session.conn,StatusLabel.NEW)
        priority_code = priority_table.get_code_by_label(session.conn,PriorityLabel.MEDIUM)
        payload = {
            "title": "Home work",
            "description": "Home work description",
            "priority_code": priority_code,
            "status_code": status_code,
            "due_date": "2030-09-23",
        }
    app_todolist.post("/v1/tasks", headers=headers, json=payload)

    res = app_todolist.get("/v1/tasks", headers=headers)
    assert res.status_code == HTTPStatus.OK
    body = res.json()
    assert body["success"] is True
    assert body["code"] == HTTPStatus.OK
    assert "tasks" in body["data"]
    assert isinstance(body["data"]["tasks"], list)
    assert any(task["title"] == "Home work" for task in body["data"]["tasks"])


def test_get_tasks_returns_internal_server_error(app_todolist):
    res = app_todolist.get("/v1/tasks")
    assert res.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert res.json()["success"] is False
    assert res.json()["message"] == "Sorry, something went wrong on our side"


# -----------------------------
# Get Task
# -----------------------------


def test_get_task_returns_ok_and_task_data(app_todolist):
    with TodolistSession() as session:
        status_code = status_table.get_code_by_label(session.conn,StatusLabel.NEW)
        priority_code = priority_table.get_code_by_label(session.conn,PriorityLabel.MEDIUM)
        payload = {
            "title": "Home work",
            "description": "Home work description",
            "priority_code": priority_code,
            "status_code": status_code,
            "due_date": "2030-09-23",
        }
    app_todolist.post("/v1/tasks", headers=headers, json=payload)

    with TodolistSession() as session:
        task_code = TaskTable.get_by_title(session.conn, "Home work")

    res = app_todolist.get(f"/v1/tasks/{task_code}", headers=headers)
    assert res.status_code == HTTPStatus.OK
    body = res.json()
    assert body["success"] is True
    assert body["data"]["title"] == "Home work"


def test_get_task_returns_bad_request_when_missing(app_todolist):
    res = app_todolist.get(f"/v1/tasks/{invalid_task_code}", headers=headers)
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json()["success"] is False
    assert res.json()["message"] == f"Task {invalid_task_code} not found"


# -----------------------------
# Update Task
# -----------------------------


def test_put_task_updates_and_returns_ok(app_todolist):
    with TodolistSession() as session:
        status_code = status_table.get_code_by_label(session.conn,StatusLabel.NEW)
        priority_code = priority_table.get_code_by_label(session.conn,PriorityLabel.MEDIUM)
        payload = {
            "title": "Home work",
            "description": "Home work description",
            "priority_code": priority_code,
            "status_code": status_code,
            "due_date": "2030-09-23",
        }
    app_todolist.post("/v1/tasks", headers=headers, json=payload)

    with TodolistSession() as session:
        task_code = TaskTable.get_by_title(session.conn, "Home work")

    new_payload = {"title": "Task updated", "due_date": "2030-09-23"}
    res = app_todolist.put(f"/v1/tasks/{task_code}", headers=headers, json=new_payload)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"success": True, "code": HTTPStatus.OK, "message": "Task updated successfully!", "data": {}}

    updated_task = app_todolist.get(f"/v1/tasks/{task_code}", headers=headers).json()
    assert updated_task["data"]["title"] == "Task updated"
    assert updated_task["data"]["due_date"] == "2030-09-23"


def test_put_task_returns_bad_request_when_missing(app_todolist):
    res = app_todolist.put(f"/v1/tasks/{invalid_task_code}", headers=headers, json={"title": "Nope"})
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json()["success"] is False
    assert res.json()["message"] == f"Task {invalid_task_code} does not exist!"


# -----------------------------
# Delete Task
# -----------------------------


def test_delete_task(app_todolist):
    with TodolistSession() as session:
        status_code = status_table.get_code_by_label(session.conn,StatusLabel.NEW)
        priority_code = priority_table.get_code_by_label(session.conn,PriorityLabel.MEDIUM)
        payload = {
            "title": "Home work",
            "description": "Home work description",
            "priority_code": priority_code,
            "status_code": status_code,
            "due_date": "2030-09-23",
        }
    app_todolist.post("/v1/tasks", headers=headers, json=payload)

    with TodolistSession() as session:
        task_code = TaskTable.get_by_title(session.conn, "Home work")

    res = app_todolist.delete(f"/v1/tasks/{task_code}", headers=headers)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"success": True, "code": HTTPStatus.OK, "message": "Task deleted successfully!", "data": {}}

    deleted_task = app_todolist.get(f"/v1/tasks/{task_code}", headers=headers)
    assert deleted_task.status_code == HTTPStatus.BAD_REQUEST
    assert deleted_task.json()["success"] is False
    assert deleted_task.json()["message"] == f"Task {task_code} not found"


def test_delete_task_returns_bad_request_when_missing(app_todolist):
    res = app_todolist.delete(f"/v1/tasks/{invalid_task_code}", headers=headers)
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json()["success"] is False
    assert res.json()["message"] == f"Task {invalid_task_code} does not exist!"
