from .auth import auth_router
from .users import user_router
from .devices import device_router
from .location import location_router
from .locationServices import locationServices_router

__init__ = [
    auth_router,
    user_router,
    device_router,
    location_router,
    locationServices_router,
]