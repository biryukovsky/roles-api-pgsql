from roles_api_pgsql.handlers import duty, v1


routes = [
    ('*', '/_health', duty.HealthHandler, 'health'),
    ('*', '/api/v1/dummy', v1.DummyHandler, 'dummy'),

    ('*', '/api/v1/role/list', v1.RolesListHandler, 'roles_list'),
    ('*', r'/api/v1/role/list/{id:\d+}', v1.RoleHandler, 'role'),
    ('*', '/api/v1/role/add', v1.CreateRoleHandler, 'create_role'),
]
