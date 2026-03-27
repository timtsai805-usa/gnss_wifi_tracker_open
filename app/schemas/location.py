from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class LocationMethod(Enum):
    gps = "gps"
    wifi = "wifi"
    lbs = "lbs"
    
class DeviceLocationBase(BaseModel):
    macs: Optional[str] = None 
    method: LocationMethod
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    accuracy: Optional[float] = None
    speed: Optional[float] = None
    motion: Optional[bool] = None
    local_time: Optional[datetime] = None

class DeviceLocationCreate(DeviceLocationBase):
    pass

class DeviceLocationResponse(DeviceLocationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes: True

class ListLocationTracksResponse(BaseModel):
    data: list[DeviceLocationResponse]
    count: int