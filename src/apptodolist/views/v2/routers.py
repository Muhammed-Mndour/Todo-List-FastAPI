from fastapi import APIRouter

from . import task, category

router = APIRouter()
router.include_router(task.router, prefix='/tasks', tags=['task'])
router.include_router(category.router, prefix='/categories', tags=['category'])
