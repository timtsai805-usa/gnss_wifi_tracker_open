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

# Create router
location_router = APIRouter(
    prefix="/location",
    tags=["Device Location"]
)

# POST device location tracks
@location_router.post("/{device_id}/tracks", response_model=DeviceLocationResponse)
async def create_device_location(
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
    
    device_location = DeviceLocation(
        user_id=user.id,
        device_id=user_device.id,
        macs=create_dl.macs,
        method=create_dl.method.value,
        latitude=create_dl.latitude,
        longitude=create_dl.longitude,
        altitude=create_dl.altitude,
        accuracy=create_dl.accuracy,
        speed=create_dl.speed,
        motion=create_dl.motion,
        local_time=create_dl.local_time,
        created_at=datetime.now(timezone.utc)
    )

    db.add(device_location)
    db.commit()
    db.refresh(device_location)

    return DeviceLocationResponse(
        id=device_location.id,
        user_id=device_location.user_id,
        device_id=device_location.device_id,
        macs=device_location.macs,
        method=device_location.method,
        latitude=device_location.latitude,
        longitude=device_location.longitude,
        altitude=device_location.altitude,
        accuracy=device_location.accuracy,
        speed=device_location.speed,
        motion=device_location.motion,
        local_time=device_location.local_time,
        created_at=device_location.created_at
    )

# GET device location tracks by date
@location_router.get("/{device_id}/tracks", response_model=ListLocationTracksResponse)
async def list_location_tracks(
    device_id: int,
    start_date: datetime,
    end_date: datetime,
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):
    
    # date time config
    start_date = datetime.combine(start_date.date(), time.min).replace(tzinfo=timezone.utc)
    end_date = datetime.combine(end_date.date(), time.max).replace(tzinfo=timezone.utc)

    # Check token if matches
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    # Check user device if exist
    user_device = (
        db.query(UserDevice)
        .filter(UserDevice.id == device_id)
        .filter(UserDevice.user_id == user.id)
        .first()
    )

    if not user_device:
        raise HTTPException(status_code=400, detail="Invalid device")

    # Check device location
    device_location = (
        db.query(DeviceLocation)
        .filter(DeviceLocation.device_id == device_id)
        .filter(DeviceLocation.created_at >= start_date)
        .filter(DeviceLocation.created_at <= end_date)
        .order_by(DeviceLocation.created_at.asc())
        .all()
    )

    data = [
        DeviceLocationResponse(
            id=dl.id,
            user_id=dl.user_id,
            method=dl.method,
            latitude=dl.latitude,
            longitude=dl.longitude, 
            altitude=dl.altitude,
            accuracy=dl.accuracy,
            speed=dl.speed,
            motion=dl.motion, 
            local_time=dl.local_time, 
            created_at=dl.created_at,
        )
        for dl in device_location
    ]

    return ListLocationTracksResponse(
        data=data,
        count=len(data)
    )