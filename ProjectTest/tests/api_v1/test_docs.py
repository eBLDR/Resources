"""
Testing main app.
"""
import pytest

from app.core.config import settings

URL = f"{settings.API_V1_URL}/docs"


@pytest.mark.anyio
async def test_docs(test_client):
    response = await test_client.get(URL)
    assert response.status_code == 200
