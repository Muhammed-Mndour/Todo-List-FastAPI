from typing import Optional

from pydantic import Field

from libutil.util import BaseModel


class ResponseBaseModel(BaseModel):
    success: bool
    code: int = 200
    message: Optional[str] = Field(default_factory=str)
    data: list[dict] = Field(default_factory=list)


class ErrorResponse(ResponseBaseModel):
    success: bool = False
    code: int
    traceback: Optional[list[str]] = None
