from roles_api_pgsql.db import manager
from roles_api_pgsql.models.role import Role


class RoleRepository:
    @classmethod
    async def get_list(cls):
        query = Role.select()
        record = await manager.execute(query)
        return record

    @classmethod
    async def create(cls, name, readable):
        record = await manager.create(Role, name=name, readable=readable)
        return record

    @classmethod
    async def get_by_id(cls, id):
        # query = Role.select(Role.id == id)
        record = await manager.get(Role, Role.id == id)
        return record

    @classmethod
    async def update(cls, role, **kwargs):
        await manager.update(role)
        return role

    @classmethod
    async def update_name(cls, role: Role, name: str):
        role.name = name
        await manager.update(role, only=(Role.name, ))
        return role

    @classmethod
    async def update_readable(cls, role: Role, readable):
        role.readable = readable
        await manager.update(role, only=(Role.readable,))
        return role

    @classmethod
    async def delete(cls, role: Role):
        await manager.delete(role)

    @classmethod
    async def delete_by_id(cls, id):
        query = Role.delete().where(Role.id == id)
        await manager.execute(query)
