from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()


@router.get('/hc')
def health_check():
    return Response("OK", status_code=200)
