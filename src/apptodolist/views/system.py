from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get('/hc')
def health_check():
    return JSONResponse("OK", status_code=200)
