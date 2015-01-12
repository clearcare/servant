from schematics.exceptions import (
        BaseError,
        ValidationError,
)


class ServantException(BaseError):
    pass


class SerializationError(ServantException):
    pass


class ActionError(ServantException):
    """General error when running an action"""
    pass

class ActionFieldError(ServantException):
    """Error for a specific action field"""
    # Used internally...user's should not raise this directly
    pass

