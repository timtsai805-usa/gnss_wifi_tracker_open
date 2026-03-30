from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class LocationMethod(Enum):
    gps = "GPS"
    wifi = "WIFI"
    lbs = "LBS"
    
class DeviceLocationBase(BaseModel):
    macs: Optional[str] = Field(
        default=None,
        max_length=255,
        description="List WiFi mac addresses",
    ) 
    method: LocationMethod = Field(
        default=None,
        description="Device location methods",
    )
    latitude: float = Field(
        default=0.0,
        description="latitude",
    )
    longitude: float = Field(
        default=0.0,
        description="longitude",
    )
    altitude: Optional[float] = Field(
        default=None,
        description="altitude"
    )
    accuracy: Optional[float] = Field(
        default=0.0,
        description="Current location accuracy",
    )
    speed: Optional[float] = Field(
        default=0.0,
        description="Current location speed",
    )
    motion: Optional[bool] = Field(
        default=None,
        description="Device motion",
    )
    local_time: Optional[datetime] = Field(
        default=None,
        description="Current location local date and time",
    )

class DeviceLocationCreate(DeviceLocationBase):
    pass

class DeviceLocationResponse(DeviceLocationBase):
    id: int
    user_id: int
    device_id: int
    created_at: datetime

    class Config:
        from_attributes: True

class ListLocationTracksResponse(BaseModel):
    data: list[DeviceLocationResponse]
    count: int