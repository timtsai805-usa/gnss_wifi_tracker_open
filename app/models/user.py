from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default=None)
    email = Column(String, unique=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)

    user_tokens = relationship("UserToken", back_populates="users")
    user_devices = relationship("UserDevice", back_populates="users")
    devices_location = relationship("DeviceLocation", back_populates="users")

class UserToken(Base):
    __tablename__ = "user_token"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)

    users = relationship("User", back_populates="user_tokens")

