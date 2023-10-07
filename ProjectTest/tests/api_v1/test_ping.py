"""
Testing ping.
"""
import pytest

from app.core.config import settings

URL = f"{settings.API_V1_URL}/ping"


@pytest.mark.anyio
async def test_ping(test_client):
    response = await test_client.get(URL)
    assert response.status_code == 200
    assert response.content == b"pong"
