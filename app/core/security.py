# JWT
# Hash password

from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
import os

from pwdlib import PasswordHash

# Get SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY")

# Token config
ALGO = "HS256"
SECRET_EXPIRE_MINUTES = 60

# Create token by user ID
def create_token(user_id: int):

    # Add expire time to this token
    expire = datetime.now(timezone.utc) + timedelta(minutes=SECRET_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

    return token, expire

# Verify token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        user_id = payload.get("sub")
        return user_id
    except JWTError:
        return None
    
# Refresh token
def refresh_token(token: str):

    # Add expire time to this token
    expire = datetime.now(timezone.utc) + timedelta(minutes=SECRET_EXPIRE_MINUTES)

    payload = {
        "sub": str(token),
        "exp": expire
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

    return token, expire

# Hash config
pwd = PasswordHash.recommended()

# Hash password
def hash_password(password: str) -> str:
    return pwd.hash(password)

# Verify password
def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(password, hashed)

