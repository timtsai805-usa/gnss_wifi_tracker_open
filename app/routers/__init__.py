from .auth import auth_router
from .users import user_router
from .devices import device_router
from .location import location_router

__init__ = [
    auth_router,
    user_router,
    device_router,
    location_router,
]