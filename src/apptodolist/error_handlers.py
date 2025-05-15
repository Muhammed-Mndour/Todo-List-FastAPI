import traceback
import typing

from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from pydantic import ValidationError as ResponseValidationError
from sqlalchemy.exc import DatabaseError
from sqlalchemy.exc import IntegrityError, OperationalError
from starlette.responses import JSONResponse

from libtodolist.exceptions import DomainException, GenericException
from libtodolist.messages.common import ErrorResponse


def generate_custom_exception_handler(
    status_code: int,
    *,
    client_error_message: typing.Union[str, typing.Callable[[Exception], str]] = str,
    include_traceback: bool = False,
):
    def err_handler(request: Request, exception: Exception) -> JSONResponse:
        client_error_msg = client_error_message(exception) if callable(client_error_message) else client_error_message
        error_message = (
            exception.message if hasattr(exception, "message") and exception.message else None
        ) or client_error_msg
        error_code = (exception.error_code if hasattr(exception, "error_code") else None) or status_code

        error_details = {
            'message': error_message,
            'code': error_code,
        }

        if include_traceback:
            error_details['traceback'] = traceback.format_exception(type(exception), exception, exception.__traceback__)

        content = ErrorResponse(**error_details).model_dump(exclude_none=True)

        return JSONResponse(content=content, status_code=status_code)

    return err_handler


def register_error_handlers(app):
    err_handler_400 = generate_custom_exception_handler(status_code=400, include_traceback=app.debug)
    err_handler_req_validation = generate_custom_exception_handler(
        status_code=400, client_error_message=str, include_traceback=app.debug
    )
    err_handler_integrity = generate_custom_exception_handler(
        status_code=400, client_error_message=str, include_traceback=app.debug
    )
    err_handler_assertion = generate_custom_exception_handler(
        status_code=400, client_error_message=str, include_traceback=app.debug
    )
    err_handler_http = generate_custom_exception_handler(
        status_code=400, client_error_message=lambda exc: exc.detail, include_traceback=app.debug
    )
    err_handler_500 = generate_custom_exception_handler(
        status_code=500, client_error_message="Sorry, something went wrong on our side", include_traceback=app.debug
    )

    app.add_exception_handler(RequestValidationError, err_handler_req_validation)
    app.add_exception_handler(AssertionError, err_handler_assertion)
    app.add_exception_handler(DomainException, err_handler_400)
    app.add_exception_handler(GenericException, err_handler_500)
    app.add_exception_handler(IntegrityError, err_handler_integrity)
    app.add_exception_handler(ResponseValidationError, err_handler_500)
    app.add_exception_handler(DatabaseError, err_handler_500)
    app.add_exception_handler(OperationalError, err_handler_500)
    app.add_exception_handler(HTTPException, err_handler_http)
    app.add_exception_handler(Exception, err_handler_500)

    return app
