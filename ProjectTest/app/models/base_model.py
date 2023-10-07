"""
Base async Data Access Layer (DAL) for SQL DB.
"""
import datetime

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.database import engine
from app.security import password_hashing

password_attr_name = "password"
updated_ts_attr_name = "updated_ts"


class BaseModel(SQLModel):
    """Base data access layer."""

    def _hash_password(self):
        """Hash model's password attribute."""
        if password := getattr(self, password_attr_name):
            setattr(self, password_attr_name, password_hashing.hash_password(password))

    async def save(self):
        """Insert new entry.
        :return: saved model
        :rtype: BaseModel
        """
        if hasattr(self, password_attr_name):
            self._hash_password()

        async_session = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with async_session() as session:
            session.add(self)
            await session.commit()
            await session.refresh(self)
            return self

    async def update(self, new_data):
        """Update existing entry.
        :return: updated model
        :rtype: BaseModel
        """
        if hasattr(self, updated_ts_attr_name):
            setattr(self, updated_ts_attr_name, datetime.datetime.utcnow())

        return await super().update(**new_data.dict())

    @classmethod
    async def find_one(cls, statement):
        """Read entry.
        :param statement: filters for select query
        :type statement: Select
        :return: found model, if any
        :rtype: BaseModel
        """
        async_session = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with async_session() as session:
            result = await session.execute(statement)
            return result.scalars().first()

    @classmethod
    async def find_one_by_id(cls, id_: int):
        """Read one entry by id.
        :param id_: entry id
        :type id_: int
        :return: found entry, if any
        :rtype: BaseModel
        """
        statement = select(cls).where(cls.id == id_)
        return await cls.find_one(statement)

    @classmethod
    async def find_all(cls):
        """Read all entries.
        :return: found entries, if any
        :rtype: list[BaseModel]
        """
        async_session = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with async_session() as session:
            result = await session.execute(select(cls))
            return result.scalars().all()

    async def delete(self):
        """Delete entry."""
        async_session = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with async_session() as session:
            await session.delete(self)
            await session.commit()
            return True
