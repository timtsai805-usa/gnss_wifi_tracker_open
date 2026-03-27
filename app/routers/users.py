from fastapi import APIRouter, HTTPException, Depends

from datetime import datetime, timezone

from app.db import SessionDep

from app.core.auth import token_validity

from app.models.user import User, UserToken

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate
)

# Create router
user_router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)

# GET user by id
@user_router.get("/me", response_model=UserResponse)
async def get_user_by_id(
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at
    )


# PUT user by id
@user_router.put("/me", response_model=UserResponse)
async def update_user_by_id(
    up_user: UserUpdate,
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):
    
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    if up_user.name is not None:
        user.name = up_user.name
    if up_user.email is not None:
        email_exist = db.query(User).filter(User.email == up_user.email, User.id != user.id).first()

        if email_exist:
            raise HTTPException(status_code=400, detail="Email already in use")
    
        user.email = up_user.email

    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at
    )

# DELETE user
@user_router.delete("/me")
async def delete_user(
    db:SessionDep,
    db_token: UserToken = Depends(token_validity)
):
    
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    db_token.revoked = True
    db.commit()

    db.delete(user)
    db.commit()
    
    # Return msg
    return {"msg": "User deleted"}