from http import HTTPStatus


class ServerException(Exception):
    def __init__(
        self, message=None, error_code=None, status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR, *, context=None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.context = context
        super().__init__(self.message)


class ClientException(Exception):
    def __init__(
        self, message=None, error_code=None, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST, *, context=None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.context = context
        super().__init__(self.message)


class UnAuthorizedActionException(ClientException):
    def __init__(self):
        self.message = "Unauthorized Action!"
        self.status_code = HTTPStatus.UNAUTHORIZED
        super().__init__(message=self.message, status_code=self.status_code)


class ForbiddenActionException(ClientException):
    def __init__(self):
        self.message = "Forbidden Action!"
        self.status_code = HTTPStatus.FORBIDDEN
        super().__init__(message=self.message, status_code=self.status_code)


class CategoryValidationException(ClientException):
    pass
