from fastapi import APIRouter

router = APIRouter()


@router.get('/tasks')
def get_tasks():
    return [
        {
            'name': "Task 1",
        },
        {
            'name': "Task 2",
        },
        {
            'name': "Task 3",
        },
    ]
