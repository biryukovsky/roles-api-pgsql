from contextlib import asynccontextmanager

import aioredis

from roles_api_pgsql.settings import _conf as config


@asynccontextmanager
async def redis_client():
    redis = await aioredis.create_redis_pool(config.config.redis_host)
    try:
        yield redis
    finally:
        redis.close()
        await redis.wait_closed()
