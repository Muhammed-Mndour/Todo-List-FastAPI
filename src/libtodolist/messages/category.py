from typing import List

from libtodolist.messages.common import ResponseBaseModel
from libutil.util import BaseModel


class Category(BaseModel):
    code: str
    label: str


class GetCategoriesResponse(ResponseBaseModel):
    data: List[Category]
