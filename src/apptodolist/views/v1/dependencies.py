from fastapi import Header, Request
from fastapi.exceptions import HTTPException

from libtodolist.context import UserContext


def get_user_context(required: bool = True):
    """
    Factory function that returns a dependency function
    with a configurable requirement for user code
    """

    def _get_user_context(user_code: str = Header(alias='X-User-Code', default=None)):
        if required and not user_code:
            raise HTTPException(status_code=401, detail="User code is required")
        return UserContext(code=user_code)

    return _get_user_context


def get_some_header(required: bool = True):
    """
    Factory function that returns a dependency function
    with a configurable requirement for some_header
    """

    def _get_some_header(request: Request):
        some_header = request.state.some_header
        if required and not some_header:
            raise HTTPException(status_code=401, detail="some_header is required")

        return some_header

    return _get_some_header
