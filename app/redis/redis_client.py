from redis.asyncio import Redis
import json
from datetime import datetime


redis_client = Redis(
    host="redis",
    port=6379,
    db=0,
    password="",
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)

async def set_key(key, value, expire=None):
    await redis_client.set(key, value, ex=expire)

async def get_key(key):
    return await redis_client.get(key)


async def save_cache_user_token(email:str, token:str, expire:datetime):
    key = f"user_token:{email}"
    data = {
        "token": token,
        "expires_at": expire.isoformat()
    }
    await set_key(
        key,
        json.dumps(data),
        expire=60*60
    )

    return True

async def get_cache_user_token(email: str):
    key = f"user_token:{email}"
    data = await get_key(key)
    if not data:
        return None
    
    return json.loads(data)