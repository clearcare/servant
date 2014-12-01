from schematics.exceptions import BaseError


class ServantException(BaseError):
    pass


class SerializationError(ServantException):
    pass


class ActionError(ServantException):
    """General error when running an action"""
    pass

class ActionFieldError(ServantException):
    """Error for a specific action field"""
    pass

