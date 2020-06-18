from peewee_async import Manager
from peewee_asyncext import PooledPostgresqlExtDatabase, PostgresqlExtDatabase

from roles_api_pgsql.settings import build_config
from roles_api_pgsql.settings import _conf as config
from roles_api_pgsql.settings import loop


build_config()


def get_pool():
    return PooledPostgresqlExtDatabase(
        database=config.config.db_name,
        max_connections=config.config.db_max_con,
        min_connections=5,
        user=config.config.db_user,
        password=config.config.db_password,
        host=config.config.db_host,
        port=config.config.db_port,
    )


def get_sync_pool():
    return PostgresqlExtDatabase(
        database=config.config.db_name,
        user=config.config.db_user,
        password=config.config.db_password,
        host=config.config.db_host,
        port=config.config.db_port,
    )


def get_manager(pool_, loop_):
    manager_ = Manager(pool_, loop=loop_)
    manager_.database.set_allow_sync(False)
    return manager_


pool = get_pool()
sync_pool = get_sync_pool()
manager = get_manager(pool, loop)
