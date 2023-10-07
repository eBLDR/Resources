"""
Declaring global shared fixtures.
"""
import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.main import app


@pytest.fixture
async def test_client():
    async with AsyncClient(app=app, base_url=settings.APP_URL) as test_client:
        yield test_client
