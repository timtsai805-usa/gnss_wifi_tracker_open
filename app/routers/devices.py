from fastapi import APIRouter, HTTPException, Depends

from datetime import datetime, timezone

from app.db import SessionDep

from app.core.auth import token_validity

from app.models.user import User, UserToken
from app.models.device import UserDevice

from app.schemas.device import (
    UserDeviceCreate,
    UserDeviceResponse,
    ListUserDeviceResponse,
    UserDeviceUpdate,
)

# Create router
device_router = APIRouter(
    prefix="/devices",
    tags=["Device Management"]
)

# POST device
@device_router.post("/", response_model=UserDeviceResponse)
async def create_device(
    create_d: UserDeviceCreate,
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):

    # Check token if matches
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    # Check imei if exist
    imei_exist = db.query(UserDevice).filter(UserDevice.imei == create_d.imei).first()
    if imei_exist:
        raise HTTPException(status_code=400, detail="Imei already exist")
    
    new_device = UserDevice(
        user_id=user.id,
        device_name=create_d.device_name,
        imei=create_d.imei,
        iccid=None,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return UserDeviceResponse(
        id=new_device.id,
        user_id=new_device.user_id,
        device_name=new_device.device_name,
        imei=new_device.imei,
        iccid=new_device.iccid,
        is_active=new_device.is_active,
        created_at=new_device.created_at
    )

# GET device by id
@device_router.get("/", response_model=ListUserDeviceResponse)
async def list_device(
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):
    
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    user_devices = db.query(UserDevice).filter(UserDevice.user_id == user.id).all()
    
    data = [
        UserDeviceResponse(
        id=ud.id,
        user_id=ud.user_id,
        device_name=ud.device_name,
        imei=ud.imei,
        iccid=ud.iccid,
        is_active=ud.is_active,
        created_at=ud.created_at
        )
        for ud in user_devices
    ]
    
    return ListUserDeviceResponse(
        data=data,
        count=len(data)
    )

# PUT device by id
@device_router.put("/{device_id}", response_model=UserDeviceResponse)
async def update_device(
    device_id: int,
    update_d: UserDeviceUpdate,
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    user_device = db.query(UserDevice).filter(UserDevice.id == device_id).first()
    if not user_device:
        raise HTTPException(status_code=404, detail="Device not found")

    if update_d.iccid is not None:
        user_device.iccid = update_d.iccid
    if update_d.device_name is not None:
        user_device.device_name = update_d.device_name

    db.commit()
    db.refresh(user_device)

    return UserDeviceResponse(
        id=user_device.id,
        user_id=user_device.user_id,
        device_name=user_device.device_name,
        imei=user_device.imei,
        iccid=user_device.iccid,
        is_active=user_device.is_active,
        created_at=user_device.created_at
    )

# DELETE device
@device_router.delete("/{device_id}")
async def delete_device(
    device_id: int,
    db: SessionDep,
    db_token: UserToken = Depends(token_validity)
):

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    user_device = db.query(UserDevice).filter(UserDevice.id == device_id).first()
    if not user_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(user_device)
    db.commit()

    return {"msg": "User device deleted"}

