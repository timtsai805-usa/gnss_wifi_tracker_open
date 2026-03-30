from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class UserDeviceBase(BaseModel):
    imei: str = Field(
        min_length=1,
        max_length=128,
        description="Device unique imei number"
    )

class UserDeviceCreate(UserDeviceBase):
    device_name: str = Field(
        min_length=1,
        max_length=255,
        description="Enter device name",
    )
    
class UserDeviceResponse(BaseModel):
    id: int
    user_id: int
    device_name: str
    imei: int
    iccid: Optional[int] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ListUserDeviceResponse(BaseModel):
    data: list[UserDeviceResponse]
    count: int

class UserDeviceUpdate(BaseModel):
    device_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Enter device name",
    )
    iccid: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=128,
        description="Device sim card number"
    )