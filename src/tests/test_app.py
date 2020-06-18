async def test_not_found(cli):
    resp = await cli.get("/")
    assert 404 == resp.status
