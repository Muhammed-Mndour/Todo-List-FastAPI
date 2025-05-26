from fastapi import Header, Request
from fastapi.exceptions import HTTPException

from libtodolist.context import RequestContext


def get_request_context(
    user_code: str = Header(
        alias='X-User-Code',
        default=None,
        include_in_schema=True,
    )
):
    return RequestContext.from_todolist_service(user_code=user_code)


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
