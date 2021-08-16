"""
Testing authentication token.
"""
import pytest

from app.core.config import settings

URL = f"{settings.API_V1_URL}/token"


@pytest.mark.asyncio
async def test_token_denied(test_client):
    data = {
        "username": "fake",
        "password": "fake",
    }
    response = await test_client.post(URL, data=data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_token_allowed(test_client, user):
    data = {
        "username": user.id,
        "password": user.id,
    }
    response = await test_client.post(URL, data=data)
    assert response.status_code == 200
