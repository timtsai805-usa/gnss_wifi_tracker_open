from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

class DeviceLocation(Base):
    __tablename__ = "devices_location"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    device_id = Column(Integer, ForeignKey("user_devices.id"), index=True)
    macs = Column(String, default=None)
    method = Column(String, default=None)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    altitude = Column(Float, default=0.0)
    accuracy = Column(Float, default=0.0)
    speed = Column(Float, default=0.0)
    motion = Column(Boolean, default=False)
    local_time = Column(DateTime, default=None)
    created_at = Column(DateTime)

    users = relationship("User", back_populates="devices_location")
    user_devices = relationship("UserDevice", back_populates="devices_location")

