from peewee import DoesNotExist, IntegrityError
from roles_api_pgsql.repos.role import RoleRepository


async def get_single_role(role_id):
    try:
        role = await RoleRepository.get_by_id(role_id)
    except DoesNotExist:
        return None
    return role


async def create_role(name, readable):
    try:
        role = await RoleRepository.create(name, readable)
        return {
            'data': {
                'id': role.id,
                'name': role.name,
                'readable': role.readable,
            }
        }
    except IntegrityError:
        return {
            'error': f'Role with name {name} already exists'
        }


async def delete_role(id):
    try:
        await RoleRepository.delete_by_id(id)
    except DoesNotExist:
        return {'success': False}
    return {'success': True}


async def update_role(role_id, name=None, readable=None):
    try:
        role = await RoleRepository.get_by_id(role_id)
    except DoesNotExist:
        return {'error': 'Role not found'}

    role.name = name or role.name
    role.readable = readable or role.readable
    try:
        role = await RoleRepository.update(role)
    except IntegrityError as e:
        return {'success': False,
                'error': str(e)}
    return {
        'success': True,
        'data': {
            'id': role.id,
            'name': role.name,
            'readable': role.readable,
        }
    }
