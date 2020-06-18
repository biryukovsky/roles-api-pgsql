import os

import click

from roles_api_pgsql.commands import cli
from roles_api_pgsql.settings import build_config


if int(os.environ.get("NEW_RELIC_ENABLE", 0)) > 0:
    import newrelic.agent
    newrelic.agent.initialize()


@cli.group()
def server():
    pass


@server.command('run')
@click.option('--log_level', default=None, show_default=True, help='Log level')
def server_run(log_level: str = None):
    build_config()
    from roles_api_pgsql.app import run
    run()
