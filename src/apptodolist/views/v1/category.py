from fastapi import APIRouter

router = APIRouter()


@router.get('/categories')
def get_categories():
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
