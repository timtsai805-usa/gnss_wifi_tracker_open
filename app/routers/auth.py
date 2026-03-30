from fastapi import APIRouter, HTTPException, Depends
from app.core.security import (create_token, refresh_token, hash_password, verify_password)

from datetime import datetime, timezone

from app.db import SessionDep

from app.core.auth import token_validity

from app.models.user import User, UserToken

from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserTokenResponse,
    UserResponse
)

from app.redis.redis_client import (
    save_cache_user_token, 
    get_cache_user_token
)


# Create router
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Sign Up
@auth_router.post("/signup", response_model=UserResponse)
async def register_user(reg_user: UserRegister, db: SessionDep):
    
    # Check if user already registered
    email_ext = db.query(User).filter(User.email == reg_user.email).first()
    if email_ext:
        raise HTTPException(status_code=400, detail="User email already exist")
    
    # Hash user password
    pwd_hash = hash_password(reg_user.password)

    # Create new user
    new_user = User(
        name=reg_user.name,
        email=reg_user.email,
        password_hash=pwd_hash,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    
    # Update user database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return user data
    return new_user

# Login
@auth_router.post("/login", response_model=UserTokenResponse)
async def login_user(login_user: UserLogin, db: SessionDep):

    # Check Cache if token exist by user email
    cached_token = await get_cache_user_token(login_user.email)
    if cached_token:
        expire = datetime.fromisoformat(cached_token["expires_at"])
        if expire > datetime.now(timezone.utc):
            return UserTokenResponse(
                token=cached_token["token"],
                expires_at=expire
                )
        
    # Check if user email matches
    db_user = db.query(User).filter(User.email == login_user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify user password
    if not verify_password(login_user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # Create user token
    token, expire = create_token(db_user.id)

    # Save to redis, TTL: 60 minutes
    await save_cache_user_token(login_user.email, token, expire)

    # Create user data
    new_login = UserToken(
        user_id=db_user.id,
        token=token,
        expires_at=expire,
        revoked=False
    )

    # Update user token database
    db.add(new_login)
    db.commit()
    db.refresh(new_login)
    
    # Return user token data
    return new_login


# Refresh Token
@auth_router.post("/refresh_token", response_model=UserTokenResponse)
async def token_refresh(
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):

    # Check if token matches
    db_token = db.query(UserToken).filter(UserToken.token == db_token.token).first()
    if not db_token:
        raise HTTPException(status_code=400, detail="Insufficient Token")
    
    # Renew token
    token, expire = refresh_token(db_token.token)

    db_token.token = token
    db_token.expires_at = expire
    db_token.revoked = False

    # Update new token only
    db.commit()

    return UserTokenResponse(
        token=db_token.token,
        expires_at=db_token.expires_at
    )


# Logout
@auth_router.post("/logout")
async def logout_user(
    db:SessionDep,
    db_token: UserToken = Depends(token_validity)
):

    # Update revoked if received token
    db_token.revoked = True
    db.commit()

    # Return msg
    return {"msg": "Logout Success"}