from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

class UserDevice(Base):
    __tablename__ = "user_devices"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    device_name = Column(String, default=None)
    imei = Column(String, unique=True)
    iccid = Column(String, default=None)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)

    users = relationship("User", back_populates="user_devices")
    devices_location = relationship("DeviceLocation", back_populates="user_devices")


