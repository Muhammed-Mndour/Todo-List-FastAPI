import random
from http import HTTPStatus

X_User_Code = "mhmd"
headers = {"X-User-Code": X_User_Code}
invalid_category_code = "fffffffff"
# -----------------------------
# Read
# -----------------------------


def test_get_categories_internal_server_error(app_todolist):
    response = app_todolist.get("/v1/categories/")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json()['success'] == False
    assert response.json()['message'] == "Sorry, something went wrong on our side"


def test_get_categories_returns_ok_and_list(app_todolist):
    label = random.choice(categories)
    app_todolist.post("/v1/categories/", headers=headers, json={'label': label})

    res = app_todolist.get("/v1/categories/", headers=headers)
    assert res.status_code == HTTPStatus.OK
    body = res.json()
    assert body["success"] is True
    assert body["code"] == HTTPStatus.OK
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


def test_post_category_creates_and_returns_ok(app_todolist):
    label = random.choice(categories)
    res = app_todolist.post("/v1/categories/", headers=headers, json={'label': label})
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"success": True, "code": HTTPStatus.OK, "message": "Category added successfully!", "data": {}}


def test_post_category_rejects_invalid_payload_with_bad_request(app_todolist):
    res = app_todolist.post("/v1/categories/", headers=headers, json={'label': '!!!!'})
    assert res.status_code == HTTPStatus.BAD_REQUEST
    body = res.json()
    assert body["success"] is False
    parsed_message = eval(body["message"])
    assert parsed_message[0]['msg'] == "Value error, label must be alphanumeric"


# -----------------------------
# Update
# -----------------------------
from src.libtodolist.db_session import TodolistSession
from src.libtodolist.data.entities import category as CategoryTable


def test_put_category_updates_and_returns_ok(app_todolist):

    label = random.choice(categories)
    post = app_todolist.post("/v1/categories/", headers=headers, json={'label': label})
    assert post.status_code == HTTPStatus.OK

    with TodolistSession() as session:
        category = CategoryTable.get_by_label(session.conn, label)
    assert category["label"] == label

    category_code = category["code"]
    assert category_code

    new_label = random.choice(categories)
    res = app_todolist.put(f"/v1/categories/{category_code}/", headers=headers, json={'label': new_label})

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "success": True,
        "code": HTTPStatus.OK,
        "message": "Category updated successfully!",
        "data": {},
    }
    with TodolistSession() as session:
        updated_category = CategoryTable.get_by_code(session.conn, category_code)

    assert updated_category["label"] == new_label


def test_put_category_returns_bad_request_when_missing(app_todolist):
    res = app_todolist.put(f"/v1/categories/{invalid_category_code}/", headers=headers, json={"label": "nope"})
    assert res.status_code == HTTPStatus.BAD_REQUEST
    body = res.json()
    assert body["success"] is False
    assert body["message"] == f"Category {invalid_category_code} does not exist!"


def test_put_category_returns_bad_request(app_todolist):
    invalid_category_code = 'invalid_category_code'
    res = app_todolist.put(f"/v1/categories/{invalid_category_code}/", headers=headers, json={"label": "nope"})
    assert res.status_code == HTTPStatus.BAD_REQUEST
    body = res.json()
    assert body["success"] is False
    assert body["message"] == f"Category {invalid_category_code} does not exist!"


# -----------------------------
# Delete
# -----------------------------


def test_delete_category_returns_ok(app_todolist):
    label = random.choice(categories)
    post = app_todolist.post("/v1/categories/", headers=headers, json={'label': label})
    assert post.status_code == HTTPStatus.OK

    with TodolistSession() as session:
        category = CategoryTable.get_by_label(session.conn, label)
    assert category["label"] == label

    category_code = category["code"]
    assert category_code

    res = app_todolist.delete(f"/v1/categories/{category_code}/", headers=headers)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {
        "success": True,
        "code": HTTPStatus.OK,
        "message": "Category deleted successfully!",
        "data": {},
    }
    with TodolistSession() as session:
        category = CategoryTable.get_by_code(session.conn, category_code, True)
    assert category is None


def test_delete_category_returns_bad_request_when_missing(app_todolist):
    res = app_todolist.delete(f"/v1/categories/{invalid_category_code}/", headers=headers)
    assert res.status_code == HTTPStatus.BAD_REQUEST
    body = res.json()
    assert body["success"] is False
    assert body["message"] == f"Category {invalid_category_code} does not exist!"
