from fastapi import APIRouter, HTTPException, Depends

from datetime import datetime, timezone, time

from app.db import SessionDep

from app.core.auth import token_validity

from app.models.user import User, UserToken
from app.models.device import UserDevice
from app.models.location import DeviceLocation

from app.schemas.location import (
    DeviceLocationCreate,
    DeviceLocationResponse,
    ListLocationTracksResponse,
)

from app.map import wifi_loc
import os


# Create router
locationServices_router = APIRouter(
    prefix="/locationServices",
    tags=["Location Services"]
)

# POST wifi location
@locationServices_router.post("/{device_id}/wifi_location")
async def request_wifi_location(
    device_id: int,
    create_dl: DeviceLocationCreate,
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):

    # Check token if matches
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    # Check user device if exist
    user_device = db.query(UserDevice).filter(UserDevice.id == device_id).first()
    if not user_device:
        raise HTTPException(status_code=400, detail="Invalid device")
    
    if create_dl.macs is not None and (
        create_dl.latitude > 0 and create_dl.longitude > 0):
        
        macs = str(create_dl.macs)
        MAP_KEY = os.getenv("MAP_KEY")

        latitude, longitude, accuracy = wifi_loc(macs, MAP_KEY)
    
    payload = DeviceLocation(
        user_id=user.id,
        device_id=user_device.id,
        macs=create_dl.macs,
        method="wifi",
        latitude=latitude,
        longitude=longitude,
        altitude=0,
        accuracy=accuracy,
        speed=create_dl.speed,
        motion=create_dl.motion,
        local_time=create_dl.local_time,
        created_at=datetime.now(timezone.utc)
    )

    db.add(payload)
    db.commit()
    db.refresh(payload)

    return DeviceLocationResponse(
        id=payload.id,
        user_id=payload.user_id,
        device_id=payload.device_id,
        macs=payload.macs,
        method=payload.method,
        latitude=payload.latitude,
        longitude=payload.longitude,
        altitude=payload.altitude,
        accuracy=payload.accuracy,
        speed=payload.speed,
        motion=payload.motion,
        local_time=payload.local_time,
        created_at=payload.created_at
    )
