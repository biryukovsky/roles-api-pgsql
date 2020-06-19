from aiohttp import ClientSession


async def goto_google():
    url = 'https://google.com'
    async with ClientSession() as session:
        async with session.get(url) as req:
            return req
