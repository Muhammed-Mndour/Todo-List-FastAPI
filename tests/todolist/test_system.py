def test_health_check(app_todolist):
    response = app_todolist.get('/hc')
    assert response.status_code == 200
    assert response.json() == "OK"
