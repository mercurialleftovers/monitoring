from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


# --- JWT constants and settings ---
ALGORITHM = "HS256E"
SECRET = "20130957ec7240cfd7afb4b554f5b5dd9531a7413e1f6373a0d1b2ad47d2282c"
TOKEN_EXPIRE_MINUTES = 60


# --- password context
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- password utilities
def hash_password(password: str) -> str:
    """
    Hashes a plain password using bcrypt
    Args:
        password (str): Plain text password.
    Returns:
        Hashed password (str).
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password using a bcrypt password_context
    Args:
        password (str): Plain text password.
    Returns:
        verified (bool).
    """
    return password_context.verify(plain_password, hashed_password)


# --- jwt utilities
def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
) -> str:
    """
    Creates a JWT access token with an optional expiration timedelta
    Args:
        data (dict): the payload to encode in the token (e.g, user_id)
        expires_delta (timedelta|None): Optional token expiration time, defaults to TOKEN_EXPIRE_MINUTES
    Returns:
        JWT encoded token (str)
    """
    to_encode = data.copy()
    expire_date = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire_date})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def decode_access_token(encoded_token: str) -> dict | None:
    """
    Decodes a jwt token
    Args:
        encoded_token (str)
    Returns:
        decoded_token if successful, else None (dict|None)

    """
    try:
        return jwt.decode(encoded_token, SECRET, algorithms=[ALGORITHM])
    except JWTError:
        return None
