from enum import StrEnum, _simple_enum

__all__ = ['HTTPMessages']

@_simple_enum(StrEnum)

class HTTPMessages:
    """HTTP custom messages to use as 'detail' of HTTPExceptions"""

    # Users endpoint
    USERNAME_DOES_NOT_EXISTS = "There is no user with that username."
    USERNAME_ALREADY_EXISTS = "Username is already registered."
    EMAIL_ALREADY_EXISTS = "Email is already registered."
    WRONG_CREDENTIALS = "Wrong Credentials! Username and/or password are incorrect."
    INVALID_PASSWORD_LENGTH = "Invalid password length."

    # Authors endpoint
    AUTHOR_DOES_NOT_EXIST = "There is no author with that name."
    AUTHOR_NAME_ALREADY_EXISTS = "Author name already used!"

    # Genres endpoint
    GENRE_DOES_NOT_EXIST = "No genre with given ID."
    GENRE_NAME_ALREADY_EXISTS = "Genre name already used!"

    # Publishers endpoint
    PUBLISHER_DOES_NOT_EXIST = "No publisher with given ID."
    PUBLISHER_NAME_ALREADY_EXISTS = "Publisher name already used!"