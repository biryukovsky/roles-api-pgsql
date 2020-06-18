from roles_api_pgsql.entities.responses import ResponseGetDummy


async def get_dummy():
    dummy = ResponseGetDummy(name="dummy",
                             nickname="nickname")
    return dummy


async def post_dummy(name: str, nickname: str = None):
    dummy = ResponseGetDummy(name=name,
                             nickname=nickname)
    return dummy
