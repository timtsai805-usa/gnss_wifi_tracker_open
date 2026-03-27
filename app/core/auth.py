# Bearer token
# Check current user

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from datetime import datetime, timezone

from app.db import SessionDep

from app.models.user import UserToken

# Bearer config
security = HTTPBearer(
    auto_error=True
)

# Check token validity from DB
def token_validity(
    db: SessionDep, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
): 

    token = credentials.credentials

    db_token = db.query(UserToken).filter(UserToken.token == token).first()
    if not db_token or db_token.revoked:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    expires_at_zone = db_token.expires_at.replace(tzinfo=timezone.utc)

    if expires_at_zone < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Token expired")
    
    return db_token