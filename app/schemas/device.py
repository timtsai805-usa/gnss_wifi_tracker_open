from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class UserDeviceBase(BaseModel):
    imei: str

class UserDeviceCreate(UserDeviceBase):
    device_name: str
    
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
    device_name: Optional[str] = None
    iccid: Optional[str] = None