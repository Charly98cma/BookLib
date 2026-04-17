from enum import StrEnum, _simple_enum

__all__ = ['HTTPMessages']

@_simple_enum(StrEnum)

class HTTPMessages:
    """HTTP custom messages to use as 'detail' of HTTPExceptions"""

    VALIDATION_ERROR: str = "Validation errors:\nField: <loc>, Error: <msg>"

    # Users endpoint
    USERNAME_DOES_NOT_EXISTS: str = "User with ID '{}' not found"
    USERNAME_ALREADY_EXISTS: str = "Username '{}' is already in use"
    EMAIL_ALREADY_EXISTS: str = "Email '{}' is already in use"
    WRONG_CREDENTIALS: str = "Wrong Credentials! Username and/or password are incorrect."
    INVALID_PASSWORD_LENGTH: str = "Invalid password length."

    # Authors endpoint
    AUTHOR_DOES_NOT_EXIST: str = "Author with ID '{}' not found"
    AUTHOR_NAME_ALREADY_EXISTS: str = "Author name already used!"

    # Genres endpoint
    GENRE_DOES_NOT_EXIST: str = "Genre with ID '{}' not found"
    GENRE_NAME_ALREADY_EXISTS: str = "Genre name already used!"

    # Publishers endpoint
    PUBLISHER_DOES_NOT_EXIST: str = "Publisher with ID '{}' not found"
    PUBLISHER_NAME_ALREADY_EXISTS: str = "Publisher name already used!"

    # Books endpoint
    BOOK_DOES_NOT_EXISTS: str = "Book with ID '{}' not found"
    BOOK_ISBN10_NOT_UNIQUE: str = "ISBN 10 '{}' already in use!"
    BOOK_ISBN13_NOT_UNIQUE: str = "ISBN 13 '{}' already in use!"
    BOOK_HC_ID_NOT_UNIQUE : str = "Hardcover ID '{}' already in use!"
