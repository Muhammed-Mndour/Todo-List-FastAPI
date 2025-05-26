from typing import Optional, List, Union

from pydantic import Field

from libutil.util import BaseModel


class ResponseBaseModel(BaseModel):
    success: bool
    code: int = 200
    message: Optional[str] = Field(default_factory=str)
    data: Union[dict, List[dict]] = Field(default_factory=dict)


class ErrorResponse(ResponseBaseModel):
    success: bool = False
    code: int
    traceback: Optional[list[str]] = None
