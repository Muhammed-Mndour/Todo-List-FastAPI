from fastapi import APIRouter

from . import task, category

router = APIRouter()
router.include_router(task.router, prefix='/task', tags=['task'])
router.include_router(category.router, prefix='/category', tags=['category'])
