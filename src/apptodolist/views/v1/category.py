from fastapi import APIRouter, Depends

from libtodolist import domain
from libtodolist.context import UserContext
from libtodolist.data import engine_todolist
from libutil.database_session import Session
from .dependencies import get_user_context

router = APIRouter()


@router.get('/categories')
def get_categories():
    return []


@router.post('/categories')
def add_category(
    req: domain.category.AddCategory,
    user_context: UserContext = Depends(get_user_context(required=True)),
):
    with Session(engine_todolist) as session:
        response = req.execute(user_context, session)
    return response


@router.put('/categories')
def update_category():
    return [
        {
            'name': "Category 1",
        },
        {
            'name': "Category 2",
        },
        {
            'name': "Category 3",
        },
    ]
