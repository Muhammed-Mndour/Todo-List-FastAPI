def test_statuses(app_todolist):
    app_todolist.post(
        '/v1/status/',
        json={'label': 'New'},
    )
    app_todolist.post(
        '/v1/status/',
        json={'label': 'In Progress'},
    )
    app_todolist.post(
        '/v1/status/',
        json={'label': 'Completed'},
    )
    app_todolist.post(
        '/v1/status/',
        json={'label': 'Canceled'},
    )
