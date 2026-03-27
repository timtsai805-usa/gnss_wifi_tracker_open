from fastapi import FastAPI

from app.routers import auth_router, user_router, device_router, location_router

from app.db import Base, engine
from app.models.user import User, UserToken
from app.models.device import UserDevice
from app.models.location import DeviceLocation

app = FastAPI(
    title="GNSS_WiFi_Tracker",
    description="This is a RESTful API built with FastAPI",
    version="1.0.0"
)

# Create table
Base.metadata.create_all(bind=engine)

# List router
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(location_router)