"""
Database connection handler.
"""
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from app.core.config import settings

engine = AsyncEngine(
    create_engine(
        settings.POSTGRESQL_URI,
        echo=True,
        future=True,
    )
)


async def init_database():
    """Initialize database and metadata."""
    from app.models.user import User

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

        # Dummy user
        user = await User.find_one_by_username(username="admin")

        if not user:
            admin_user = User(
                username="admin",
                password="1234",
                email="admin@admin.com",
            )
            await admin_user.save()


async def get_session() -> AsyncSession:
    """Yields a fresh database session."""
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
