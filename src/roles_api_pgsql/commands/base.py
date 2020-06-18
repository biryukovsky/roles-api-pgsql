import asyncio
from functools import update_wrapper

import click


def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return update_wrapper(wrapper, f)


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass
