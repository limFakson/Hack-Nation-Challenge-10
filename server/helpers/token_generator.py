import jwt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any

# --- JWT Configuration ---
# You would typically store this in environment variables.
SECRET_KEY = "your-secret-key"  # Change this to a secure, random string
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 60 * 60

# --- Helper Functions for Token Management ---


def create_access_token(data: Dict[str, Any]):
    """
    Generates a new JWT token containing the user's ID and name,
    with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decodes a JWT token and returns the payload if valid.
    Raises an HTTPException if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
