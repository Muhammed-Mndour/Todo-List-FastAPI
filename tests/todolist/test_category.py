# def test_post_category(app_todolist):
#     response = app_todolist.post("/v1/categories/", headers={"X-User-Code": "mhmd"}, json={'label': 'Work'})


# -----------------------------
# Read
# -----------------------------


def test_get_categories_500_error_body(app_todolist):
    response = app_todolist.get("/v1/categories/")
    assert response.status_code == 500
    assert response.json()['success'] == False
    assert response.json()['message'] == "Sorry, something went wrong on our side"


def test_get_categories_returns_200_and_list(app_todolist):
    label = random.choice(categories)
    app_todolist.post("/v1/categories/", headers={"X-User-Code": "mhmd"}, json={'label': label})

    res = app_todolist.get("/v1/categories/", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["code"] == 200
    assert body["message"] == ""
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 1
    assert body["data"][0]["label"] == label
    assert isinstance(body["data"][0]["code"], str)  # code is dynamic, just check type


# Create
# -----------------------------

categories = [
    "Health",
    "Sports",
    "Education",
    "Entertainment",
    "Technology",
    "Travel",
    "Food",
    "Finance",
    "Hobbies",
]

import random


def test_post_category_creates_and_returns_200(app_todolist):
    label = random.choice(categories)
    res = app_todolist.post("/v1/categories/", headers={"X-User-Code": "mhmd"}, json={'label': label})
    assert res.status_code == 200
    assert res.json() == {"success": True, "code": 200, "message": "Category added successfully!", "data": {}}


def test_post_category_rejects_invalid_payload_with_400(app_todolist):
    res = app_todolist.post("/v1/categories/", headers={"X-User-Code": "mhmd"}, json={'label': '!!!!'})
    assert res.status_code == 400
    body = res.json()
    assert body["success"] is False
    parsed_message = eval(body["message"])
    assert parsed_message[0]['msg'] == "Value error, label must be alphanumeric"


# -----------------------------
# Update
# -----------------------------
from src.libtodolist.db_session import TodolistSession
from src.libtodolist.data.entities import category as CategoryTable


def test_put_category_updates_and_returns_200(app_todolist):

    label = random.choice(categories)
    post = app_todolist.post("/v1/categories/", headers={"X-User-Code": "mhmd"}, json={'label': label})
    assert post.status_code == 200

    with TodolistSession() as session:
        category = CategoryTable.get_by_label(session.conn, label)
    assert category["label"] == label

    category_code = category["code"]
    assert category_code

    new_label = random.choice(categories)
    res = app_todolist.put(
        f"/v1/categories/{category_code}/", headers={"X-User-Code": "mhmd"}, json={'label': new_label}
    )

    assert res.status_code == 200
    assert res.json() == {"success": True, "code": 200, "message": "Category updated successfully!", "data": {}}
    with TodolistSession() as session:
        updated_category = CategoryTable.get_by_code(session.conn, category_code)

    assert updated_category["label"] == new_label


def test_put_category_returns_400_when_missing(app_todolist):
    res = app_todolist.put("/v1/categories/fffffff/", headers={"X-User-Code": "mhmd"}, json={"label": "nope"})
    assert res.status_code == 400
    body = res.json()
    assert body["success"] is False
    assert body["message"] == "Category fffffff does not exist!"


# -----------------------------
# Delete
# -----------------------------


def test_delete_category_returns_200(app_todolist):
    label = random.choice(categories)
    post = app_todolist.post("/v1/categories/", headers={"X-User-Code": "mhmd"}, json={'label': label})
    assert post.status_code == 200

    with TodolistSession() as session:
        category = CategoryTable.get_by_label(session.conn, label)
    assert category["label"] == label

    category_code = category["code"]
    assert category_code

    res = app_todolist.delete(f"/v1/categories/{category_code}/", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 200
    assert res.json() == {"success": True, "code": 200, "message": "Category deleted successfully!", "data": {}}
    with TodolistSession() as session:
        category = CategoryTable.get_by_code(session.conn, category_code,True)
    assert category is None


def test_delete_category_returns_400_when_missing(app_todolist):
    res = app_todolist.delete("/v1/categories/fffffff/", headers={"X-User-Code": "mhmd"})
    assert res.status_code == 400
    body = res.json()
    assert body["success"] is False
    assert body["message"] == "Category fffffff does not exist!"
