from .user import (
    UserResponse,
    UserUpdate,
    UserRegister,
    UserTokenResponse,
    UserLogin,
)

from .device import (
    UserDeviceCreate,
    UserDeviceResponse,
    UserDeviceUpdate,
    ListUserDeviceResponse,
)

from .location import (
    DeviceLocationCreate,
    DeviceLocationResponse,
    ListLocationTracksResponse,
)

__init__ = [
    UserResponse,
    UserUpdate,
    UserRegister,
    UserTokenResponse,
    UserLogin,
    
    UserDeviceCreate,
    UserDeviceResponse,
    UserDeviceUpdate,
    ListUserDeviceResponse,

    DeviceLocationCreate,
    DeviceLocationResponse,
    ListLocationTracksResponse,
]