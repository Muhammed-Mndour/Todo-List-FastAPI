from fastapi import APIRouter

from .system import router as system_router
from .v1.routers import router as router_v1
from .v2.routers import router as router_v2

router = APIRouter()
router.include_router(system_router, tags=['system'])
router.include_router(router_v1, prefix='/v1', tags=['v1'])
router.include_router(router_v2, prefix='/v2', tags=['v2'])
