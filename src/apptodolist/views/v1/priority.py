from src.libtodolist.db_session import TodolistSession
from fastapi import APIRouter
from libtodolist import domain
from src.libtodolist.messages.common import ResponseBaseModel

router = APIRouter()


@router.post('')
def add_priority(msg: domain.priority.AddPriority):
    with TodolistSession() as session:
        msg.execute(session)
    return ResponseBaseModel(success=True, message="Priority added successfully!")
