from fastapi import APIRouter, Depends

from libtodolist import domain
from libtodolist.context import RequestContext
from libtodolist.db_session import TodolistSession
from libtodolist.messages.category import GetCategoriesResponse
from libtodolist.messages.common import ResponseBaseModel
from .dependencies import get_request_context

router = APIRouter()


@router.get('')
def get_categories(
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        categories = domain.category.GetCategories().execute(ctx, session)
    return GetCategoriesResponse(success=True, data=categories)


@router.post('')
def add_category(
    msg: domain.category.AddCategory,
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        msg.execute(ctx, session)
    return ResponseBaseModel(success=True, message="Category added successfully!")


@router.put('/{code}')
def update_category(
    msg: domain.category.UpdateCategory = Depends(),
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        msg.execute(ctx, session)
    return ResponseBaseModel(success=True, message="Category updated successfully!")


@router.delete('/{code}')
def delete_category(
    msg: domain.category.DeleteCategory = Depends(),
    ctx: RequestContext = Depends(get_request_context),
):
    with TodolistSession() as session:
        msg.execute(ctx, session)
    return ResponseBaseModel(success=True, message="Category deleted successfully!")
