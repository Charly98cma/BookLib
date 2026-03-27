from enum import StrEnum, _simple_enum

__all__ = ['HTTPMessages']

@_simple_enum(StrEnum)

class HTTPMessages:
    """HTTP custom messages to use as 'detail' of HTTPExceptions"""

    # User endpoint
    USERNAME_DOES_NOT_EXISTS = "There is no user with that username."
    USERNAME_EMAIL_ALREADY_EXISTS = "An user with that username or email already exists."
    WRONG_CREDENTIALS = "Wrong Credentials! Username and/or password are incorrect."
    INVALID_PASSWORD_LENGTH = "Invalid password length."
