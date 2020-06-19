from aiocache import SimpleMemoryCache
from aiocache.serializers import JsonSerializer
from aiohttp import web
from aiohttp_apispec import docs, response_schema, use_kwargs
from marshmallow import ValidationError

from roles_api_pgsql.entities.requests import RequestPostDummy
from roles_api_pgsql.entities.responses import ResponseGetDummyData, ResponseGetDummy, \
    ResponseInternalError
from roles_api_pgsql.services.dummy import get_dummy, post_dummy
from roles_api_pgsql.services.role import (get_role_list, get_single_role,
                                           create_role, delete_role,
                                           update_role, )


cache = SimpleMemoryCache(serializer=JsonSerializer())


class DummyHandler(web.View):
    @docs(tags=['dummy'],
          summary='Get dummy',
          description='''Dummy resource''')
    @response_schema(ResponseGetDummyData.Schema(), 200, description="Single dummy", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    async def get(self):
        dummy = await get_dummy()
        try:
            payload = dummy.make_dump()
        except ValidationError as err:
            return web.json_response({"error": err.messages}, status=400)
        return web.json_response({"data": payload})


    @docs(tags=['dummy'],
          summary='Post new dummy',
          description='''Dummy resource''')
    @use_kwargs(RequestPostDummy.Schema())
    @response_schema(ResponseGetDummyData.Schema(), 200, description="Single dummy", required=True)
    @response_schema(ResponseInternalError.Schema(), 400, description="Error description", required=True)
    async def post(self):
        request_entity: RequestPostDummy  # for typing
        request_entity = self.request['validated_data']

        dummy = await post_dummy(request_entity.name, request_entity.nickname)  # if not nick_name in req, return none
        try:
            payload = dummy.make_dump()
        except ValidationError as err:
            return web.json_response({"error": err.messages}, status=400)
        return web.json_response({"data": payload})


class RolesListHandler(web.View):
    async def get(self):
        resp = await get_role_list()
        return web.json_response({'data': resp})


class RoleHandler(web.View):
    async def get(self):
        role_id = int(self.request.match_info['id'])
        role = await get_single_role(role_id)
        if role is not None:
            return web.json_response({
                'data': {
                    'id': role.id,
                    'name': role.name,
                    'readable': role.readable,
                }
            })
        return web.json_response({'error': 'Role not found'}, status=404)

    async def patch(self):
        role_id = int(self.request.match_info['id'])
        req_data = await self.request.json()
        resp = await update_role(role_id,
                                 name=req_data.get('name'),
                                 readable=req_data.get('readable'))
        return web.json_response(resp)

    async def delete(self):
        role_id = int(self.request.match_info['id'])
        resp = await delete_role(role_id)
        if not resp['success']:
            return web.json_response(resp, status=404)
        return web.json_response(resp)


class CreateRoleHandler(web.View):
    async def post(self):
        req_data = await self.request.json()
        name = req_data.get('name')
        readable = req_data.get('readable')
        if not name or not readable:
            return web.json_response({'error': 'name and readable are required fields'},
                                     status=400)
        resp = await create_role(name, readable)
        return web.json_response(resp)
