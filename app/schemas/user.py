from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

# Auth
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    
class UserLogin(UserRegister):
    pass

class UserTokenResponse(BaseModel):
    token: str
    expires_at: datetime

    class Config:
        from_attributes: True

class RefreshToken(BaseModel):
    token: str

# User
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes: True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# User Device
class UserDeviceBase(BaseModel):
    user_id: int
    device_id: int

class UserDeviceCreate(UserDeviceBase):
    user_name: str
    device_nme: str

class UserDeviceResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    user_name: str
    device_name: str
    is_share: bool
    created_at: datetime

    class Config:
        from_attributes: True

class UserDeviceUpdate(BaseModel):
    user_name: Optional[str]
    device_name: Optional[str]
    is_share: Optional[bool]

