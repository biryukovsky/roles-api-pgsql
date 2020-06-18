import importlib
import inspect
import os

import click
from ptpython.repl import embed

from roles_api_pgsql.commands import cli
from roles_api_pgsql.models.base import BaseModel


@cli.command('shell')
@click.option('--sqldebug', default=False, is_flag=True, help='Show all queries made by ORM')
def shell(sqldebug):
    models = importlib.import_module('roles_api_pgsql.models', package='roles_api_pgsql')
    locals_d = dict(models=models)
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and issubclass(obj, BaseModel):
            locals_d[name] = obj
    if sqldebug:
        models.sql_debug(True)

    for name, obj in inspect.getmembers(models):
        locals_d[name] = obj

    embed(
        globals=locals_d,
        vi_mode=True,
        history_filename=os.path.join(os.path.expanduser('~'), '.roles_api_pgsql_cli_history'),
        title='roles_api_pgsql server shell',
    )
