def test_post_category(app_todolist):
    response = app_todolist.post('/v1/categories/', headers={"X-User-Code": "mhmd"}, json={'label': 'Work'})
    assert response.status_code == 200
    assert response.json() == {"success": True, "code": 200, "message": "Category added successfully!", "data": {}}
