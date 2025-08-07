def test_priorities(app_todolist):
    app_todolist.post(
        '/v1/priority/',
        json={'label': 'Low'},
    )
    app_todolist.post(
        '/v1/priority/',
        json={'label': 'Medium'},
    )
    app_todolist.post(
        '/v1/priority/',
        json={'label': 'High'},
    )
