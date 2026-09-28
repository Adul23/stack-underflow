# apps/chat/rate_limit.py
from time import time

from redis.asyncio import Redis

from stack_underflow.base import REDIS_HOST, REDIS_PORT

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=2)


async def is_rate_limited(user_id, max_messages=20, window_seconds=60):
    key = f"rate_limit:ws:{user_id}"
    now = time()
    pipe = redis_client.pipeline()
    pipe.zremrangebyscore(key, 0, now - window_seconds)
    pipe.zadd(key, {f"{now}": now})
    pipe.zcard(key)
    pipe.expire(key, window_seconds)
    results = await pipe.execute()
    message_count = results[2]
    return message_count > max_messages
