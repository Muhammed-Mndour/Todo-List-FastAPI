from src.libtodolist.db_session import TodolistSession
from fastapi import APIRouter
from libtodolist import domain
from src.libtodolist.messages.common import ResponseBaseModel

router = APIRouter()


@router.post('')
def add_status(msg: domain.status.AddStatus):
    with TodolistSession() as session:
        msg.execute(session)
    return ResponseBaseModel(success=True, message="Status added successfully!")
