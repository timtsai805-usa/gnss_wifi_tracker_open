from fastapi import FastAPI

from app.routers import auth_router, user_router, device_router, location_router, locationServices_router

from app.db import Base, engine
from app.models.user import User, UserToken
from app.models.device import UserDevice
from app.models.location import DeviceLocation

import os
from dotenv import load_dotenv

app = FastAPI(
    title="GNSS_WiFi_Tracker",
    description="This is a RESTful API built with FastAPI",
    version="1.0.0"
)

# Load keys from env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
MAP_KEY = os.getenv("MAP_KEY")
MAP_URL = os.getenv("MAP_URL")

# Create table
Base.metadata.create_all(bind=engine)

# List router
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(location_router)
app.include_router(locationServices_router)