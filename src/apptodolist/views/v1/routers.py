from fastapi import APIRouter

from . import task, category, status, priority

router = APIRouter()
router.include_router(task.router, prefix='/tasks', tags=['task'])
router.include_router(category.router, prefix='/categories', tags=['category'])
router.include_router(status.router, prefix='/status', tags=['status'])
router.include_router(priority.router, prefix='/priority', tags=['priority'])
