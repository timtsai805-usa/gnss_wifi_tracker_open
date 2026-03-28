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

from app.services.map import process_wifi_location, process_location_address
import os


# Create router
locationServices_router = APIRouter(
    prefix="/locationServices",
    tags=["Location Services"]
)

# POST wifi location
@locationServices_router.post("/{device_id}/wifi_location", response_model=DeviceLocationResponse)
async def get_device_wifi_location(
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
        raise HTTPException(status_code=400, detail="Insufficient user device")
    
    if create_dl.macs is not None and (
        create_dl.latitude >= 0 and create_dl.longitude >= 0):
        
        macs = str(create_dl.macs)
        latitude, longitude, accuracy = process_wifi_location(macs)

    else:
        raise HTTPException(status_code=400, detail="Invalid wifi data")
    
    lat_lng = f"{latitude},{longitude}"
    try:
        format_address = process_location_address(lat_lng)
    except:
        raise HTTPException(status_code=400, detail="Insufficient address request")
    
    data = DeviceLocation(
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
        address=format_address,
        created_at=datetime.now(timezone.utc)
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return data
