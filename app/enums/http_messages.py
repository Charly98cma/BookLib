from enum import StrEnum, _simple_enum

__all__ = ['HTTPMessages']

@_simple_enum(StrEnum)

class HTTPMessages:
    """HTTP messages to use as detail of HTTPExceptions"""

    # USER
    USERNAME_DOES_NOT_EXISTS = "There is no user with that username"
    USERNAME_ALREADY_EXISTS = "An user with that username already exists!"
    EMAIL_ALREADY_EXISTS = "An user with that email already exists!"
    WRONG_CREDENTIALS = "Wrong Credentials!\nUsername and/or password are incorrect!"
