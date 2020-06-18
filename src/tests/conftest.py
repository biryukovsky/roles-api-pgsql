import asyncio
import logging
import random
import re

import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import DynamicResource
from faker import Faker
from mock import patch

from roles_api_pgsql.settings import Settings

fake = Faker()


def dummy_settings():
    return Settings(**dict(
        listen_port=fake.pyint(),
        listen_host=fake.ipv4(),
        db_name=fake.slug(),
        db_max_con=fake.pyint(),
        db_user=fake.user_name(),
        db_password=fake.password(),
        db_host=fake.hostname(),
        db_port=fake.pyint(),
        log_level=random.choice(list(logging._nameToLevel))
        ))


@pytest.fixture(scope='session')
def faker():
    return fake


@pytest.fixture(scope='session', autouse=True)
def config():
    with patch('roles_api_pgsql.settings._conf.config', dummy_settings()):
        yield


@pytest.fixture(scope='session')
def loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop
    loop.close()


@pytest.fixture(scope='session')
@patch("roles_api_pgsql.settings.build_config", scope="session")
def manager(loop, mock_config):
    mock_config.return_value = None
    from roles_api_pgsql.db import get_manager, pool
    return get_manager(pool, loop)


@pytest.fixture
@patch("roles_api_pgsql.settings.build_config", scope="session")
def cli(mock_config, loop, aiohttp_client):
    app = web.Application()
    from roles_api_pgsql.app import make_app
    app_ready = make_app(app)
    return loop.run_until_complete(aiohttp_client(app_ready))


@pytest.fixture
async def route_path(cli):
    def _router_path(router_name, param=''):
        resource = cli.server.app.router[router_name]

        if isinstance(resource, DynamicResource):
            result = re.sub(r"{.+}", param, resource._formatter)
        else:
            result = resource._path

        return result

    return _router_path
