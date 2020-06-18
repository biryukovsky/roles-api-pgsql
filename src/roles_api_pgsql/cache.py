from aiocache import SimpleMemoryCache

from roles_api_pgsql.settings import build_config


build_config()


def setup_cache():
    cache = SimpleMemoryCache(ttl=10)
    return cache


cache = setup_cache()
