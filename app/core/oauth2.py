import bcrypt

################################################################################

PASSWD_ENCODING = "utf-8"

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(PASSWD_ENCODING), bcrypt.gensalt()).decode(PASSWD_ENCODING)

def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode(PASSWD_ENCODING),
        hashed.encode(PASSWD_ENCODING),
    )

################################################################################

def create_access_token():
    pass

def create_refresh_token():
    pass

def decode_token():
    pass
