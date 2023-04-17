import pytest


@pytest.mark.anyio
async def test_initial_response(create_test_client):
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Home" in str(body)
