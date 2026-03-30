from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

# Auth
class UserRegister(BaseModel):
    email: EmailStr = Field(
        max_length=255,
        description="Enter your email address"
    )
    password: str = Field(
        min_length=8,
        max_length=255,
        description="Enter min. 8-digits password",
    )
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=128,
        description="Enter user name",
    )
    
class UserLogin(BaseModel):
    email: EmailStr = Field(
        max_length=255,
        description="Enter your email address"
    )
    password: str = Field(
        min_length=8,
        max_length=255,
        description="Enter min. 8-digits password",
    )

class UserTokenResponse(BaseModel):
    token: str
    expires_at: datetime

    class Config:
        from_attributes: True

# User
class UserBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=128,
        description="Enter user name",
    )
    email: EmailStr = Field(
        max_length=255,
        description="Enter your email address"
    )
    
class UserResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes: True

class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=128,
        description="Enter user name",
    )
    email: Optional[EmailStr] = Field(
        default=None,
        max_length=255,
        description="Enter your email address"
    )
