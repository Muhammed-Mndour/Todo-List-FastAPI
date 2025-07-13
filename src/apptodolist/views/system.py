from fastapi import APIRouter

from libtodolist.messages.common import ResponseBaseModel

router = APIRouter()


@router.get('/hc')
def health_check():
    return ResponseBaseModel(success=True, message="Health check passed!")
