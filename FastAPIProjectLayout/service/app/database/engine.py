"""
Database session client.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.core.config import settings


class Database:
    """Database connection handler."""
    client: AsyncIOMotorClient
    engine: AIOEngine


def open_connection():
    """Opening database client session."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.engine = AIOEngine(
        motor_client=db.client,
        database=settings.MONGODB_DB_NAME,
    )


def close_connection():
    """Closing database client session."""
    db.client.close()


db = Database()
