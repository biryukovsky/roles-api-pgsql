from aiocache import SimpleMemoryCache
from aiocache.serializers import JsonSerializer
from aiohttp import web

from roles_api_pgsql.settings import represent_conf


cache = SimpleMemoryCache(serializer=JsonSerializer())


class HealthHandler(web.View):
    async def get(self):
        return web.json_response(dict(data=represent_conf()))
