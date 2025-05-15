class GenericException(Exception):
    def __init__(self, message=None, error_code=None, *, context=None):
        self.message = message
        self.error_code = error_code
        self.context = context
        super().__init__(self.message)


class DomainException(Exception):
    def __init__(self, message=None, error_code=None, *, context=None):
        self.message = message
        self.error_code = error_code
        self.context = context
        super().__init__(self.message)
