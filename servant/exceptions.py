from schematics.exceptions import BaseError


class ServantException(BaseError):
    pass


class SerializationError(ServantException):
    pass


class ActionFieldError(ServantException):
    pass
