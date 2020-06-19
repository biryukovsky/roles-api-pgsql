from dataclasses import asdict, dataclass
import os
import threading

import uvloop
import asyncio


uvloop.install()
loop = asyncio.get_event_loop()

_conf = threading.local()
_conf.config = None


@dataclass(frozen=True)
class Settings:
    db_name: str = os.getenv('DB_NAME')
    db_max_con: int = int(os.getenv('DB_MAX_CON'))
    db_user: str = os.getenv('DB_USER')
    db_password: str = os.getenv('DB_PASSWORD')
    db_host: str = os.getenv('DB_HOST')
    db_port: int = int(os.getenv('DB_PORT'))
    listen_port: int = int(os.getenv('LISTEN_PORT'))
    listen_host: str = os.getenv('LISTEN_HOST')
    log_level: str = os.getenv('LOG_LEVEL')
    redis_host: str = os.getenv('REDIS_HOST')


def build_config():
    if _conf.config:
        return _conf.config
    # settings = Settings.create()
    _conf.config = Settings()
    return _conf.config


def represent_conf():
    skip_suffixes = ['password', 'secret']
    return {
        key: value for key, value in asdict(_conf.config).items()
        if all(key.find(skip) < 0 for skip in skip_suffixes)
    }
