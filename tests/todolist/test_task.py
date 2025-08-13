import random
from src.libtodolist.db_session import TodolistSession
from src.libtodolist.data.entities import task as TaskTable

# -----------------------------
# Create Task
# -----------------------------


def test_post_task_creates_and_returns_200(app_todolist):
    payload = {
        "title": "Home work",
        "description": "Home work description",
        "priority_code": "PMed456789",
        "status_code": "SNew456789",
        "due_date": "2030-09-23",
    }
    res = app_todolist.post("/v1/tasks", headers={"X-User-Code": "mhmd"}, json=payload)
    assert res.status_code == 200
    assert res.json() == {"success": True, "code": 200, "message": "Task added successfully!", "data": {}}


def test_post_task_rejects_empty_title_with_400(app_todolist):
    payload = {"title": ""}
    res = app_todolist.post("/v1/tasks", headers={"X-User-Code": "mhmd"}, json=payload)
    assert res.status_code == 400
    body = res.json()
    assert body["success"] is False
    parsed_message = eval(body["message"])
    assert parsed_message[0]['msg'] == "Value error, title must not be empty"


# -----------------------------
# Get Tasks
# -----------------------------


def test_get_tasks_returns_200_and_list(app_todolist):
    payload = {
        "title": "Home work",
        "description": "Home work description",
        "priority_code": "PMed456789",
        "status_code": "SNew456789",
        "due_date": "2030-09-23",
    }
    app_todolist.post("/v1/tasks", headers={"X-User-Code": "mhmd"}, json=payload)

    res = app_todolist.get("/v1/tasks", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["code"] == 200
    assert "tasks" in body["data"]
    assert isinstance(body["data"]["tasks"], list)
    assert any(task["title"] == "Home work" for task in body["data"]["tasks"])


def test_get_tasks_returns_500_on_server_error(app_todolist):
    res = app_todolist.get("/v1/tasks")
    assert res.status_code == 500
    assert res.json()["success"] is False
    assert res.json()["message"] == "Sorry, something went wrong on our side"


# -----------------------------
# Get Task
# -----------------------------


def test_get_task_returns_200_and_task_data(app_todolist):
    payload = {
        "title": "Home work",
        "description": "Home work description",
        "priority_code": "PMed456789",
        "status_code": "SNew456789",
        "due_date": "2030-09-23",
    }
    app_todolist.post("/v1/tasks", headers={"X-User-Code": "mhmd"}, json=payload)

    with TodolistSession() as session:
        task_code = TaskTable.get_by_title(session.conn, "Home work")

    res = app_todolist.get(f"/v1/tasks/{task_code}", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["data"]["title"] == "Home work"


def test_get_task_returns_400_when_missing(app_todolist):
    res = app_todolist.get("/v1/tasks/fffffff", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 400
    assert res.json()["success"] is False
    assert res.json()["message"] == "Task fffffff not found"


# -----------------------------
# Update Task
# -----------------------------


def test_put_task_updates_and_returns_200(app_todolist):
    payload = {
        "title": "Home work",
        "description": "Home work description",
        "priority_code": "PMed456789",
        "status_code": "SNew456789",
        "due_date": "2030-09-23",
    }
    app_todolist.post("/v1/tasks", headers={"X-User-Code": "mhmd"}, json=payload)

    with TodolistSession() as session:
        task_code = TaskTable.get_by_title(session.conn, "Home work")

    new_payload = {"title": "Task updated", "due_date": "2030-09-23"}
    res = app_todolist.put(f"/v1/tasks/{task_code}", headers={"X-User-Code": "mhmd"}, json=new_payload)
    assert res.status_code == 200
    assert res.json() == {"success": True, "code": 200, "message": "Task updated successfully!", "data": {}}

    updated_task = app_todolist.get(f"/v1/tasks/{task_code}", headers={"X-User-Code": "mhmd"}).json()
    assert updated_task["data"]["title"] == "Task updated"
    assert updated_task["data"]["due_date"] == "2030-09-23"


def test_put_task_returns_400_when_missing(app_todolist):
    res = app_todolist.put("/v1/tasks/fffffff", headers={"X-User-Code": "mhmd"}, json={"title": "Nope"})
    assert res.status_code == 400
    assert res.json()["success"] is False
    assert res.json()["message"] == "Task fffffff does not exist!"


# -----------------------------
# Delete Task
# -----------------------------


def test_delete_task_returns_200(app_todolist):
    payload = {
        "title": "Home work",
        "description": "Home work description",
        "priority_code": "PMed456789",
        "status_code": "SNew456789",
        "due_date": "2030-09-23",
    }
    app_todolist.post("/v1/tasks", headers={"X-User-Code": "mhmd"}, json=payload)

    with TodolistSession() as session:
        task_code = TaskTable.get_by_title(session.conn, "Home work")

    res = app_todolist.delete(f"/v1/tasks/{task_code}", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 200
    assert res.json() == {"success": True, "code": 200, "message": "Task deleted successfully!", "data": {}}

    deleted_task = app_todolist.get(f"/v1/tasks/{task_code}", headers={"X-User-Code": "mhmd"})
    assert deleted_task.status_code == 400
    assert deleted_task.json()["success"] is False
    assert deleted_task.json()["message"] == f"Task {task_code} not found"


def test_delete_task_returns_400_when_missing(app_todolist):
    res = app_todolist.delete("/v1/tasks/fffffff", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 400
    assert res.json()["success"] is False
    assert res.json()["message"] == "Task fffffff does not exist!"
