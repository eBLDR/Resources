"""
Declaring global shared fixtures.
"""
import asyncio

import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.database.engine import close_connection, db, open_connection
from main import app


@pytest.fixture
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture
def database(request):
    open_connection()
    yield db

    def teardown():
        close_connection()
        db.client.drop_database(settings.MONGODB_DB_NAME)

    request.addfinalizer(teardown)


@pytest.fixture
async def test_client(database):
    async with AsyncClient(app=app, base_url=settings.APP_URL) as test_client:
        yield test_client


@pytest.fixture
async def user():
    return await _user("admin", "admin")


async def _user(username, password):
    user = None  # Fill me
    return user


@pytest.fixture
async def token_user(user):
    return await _get_headers(user.id, user.id)


async def _get_headers(username, password):
    url = "/token"
    data = {
        "username": username,
        "password": password,
    }

    async with AsyncClient(app=app, base_url=settings.APP_URL) as client:
        response = await client.post(url, data=data)

    return {
        "Authorization": f"Bearer {response.json().get('access_token')}",
    }
