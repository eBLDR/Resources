"""
Base DAO for NoSQL collections using odmantic.AIOEngine.
"""
import datetime
from typing import Union

from bson.objectid import ObjectId
from odmantic.query import QueryExpression, SortExpression

from app.database.engine import db
from app.schemas.base import BaseSchema
from app.security import password_hashing
from helpers.util_exception import BaseCustomException


class ValidationError(BaseCustomException):
    """Raised when data validation fails."""


class MissingReferenceError(ValidationError):
    """Raised when there is a missing reference."""

    def __init__(self, resource_name, resource_id):
        msg = f"Missing reference: {resource_name} ({resource_id})"
        super().__init__(msg)


class BaseDAO:
    """Base data access object."""
    model = NotImplemented

    @staticmethod
    def hash_password(document):
        """Hash password attribute.
        :param document: document's model
        :type document: cls.model
        """
        if password := getattr(document, "password"):
            document.password = password_hashing.hash_password(password)

    @classmethod
    async def save(cls, document: model):
        """(Upsert) Insert new document or update existing.
        :param document: document's model to be saved
        :type document: cls.model
        :return: saved document
        :rtype: cls.model
        """
        if hasattr(cls, "validate_references") and callable(cls.validate_references):
            await cls.validate_references(document)

        if hasattr(document, "password"):
            cls.hash_password(document)
        return await db.engine.save(document)

    @classmethod
    async def save_from_schema(cls, schema: BaseSchema):
        """(Upsert) Insert new document or update existing from schema.
        :param schema: schema with document's data
        :type schema: BaseSchema
        :return: saved document
        :rtype: cls.model
        """
        return await cls.save(
            schema.to_document(
                cls.model,
            ),
        )

    @classmethod
    async def find_one_by_id(cls, document_id: Union[ObjectId, str, int]):
        """Read document.
        :param document_id: document id
        :type document_id: Union[ObjectId, str, int)]
        :return: found document, if any
        :rtype: cls.model
        """
        return await cls.find_one(
            cls.model.id == document_id,
        )

    @classmethod
    async def find_one(cls, *query_expressions: QueryExpression):
        """Read document.
        :param query_expressions: query expressions
        :type query_expressions: tuple(QueryExpression)
        :return: found document, if any
        :rtype: cls.model
        """
        return await db.engine.find_one(
            cls.model,
            *query_expressions or {},
        )

    @classmethod
    async def find(
            cls,
            *query_expressions: QueryExpression,
            sort: SortExpression = None,
    ):
        """Read documents.
        :param query_expressions: query expressions
        :type query_expressions: tuple(QueryExpression)
        :param sort: sort expression
        :type sort: SortExpression
        :return: found documents, if any
        :rtype: list[cls.model]
        """
        return await db.engine.find(
            cls.model,
            *query_expressions or {},
            sort=sort,
        )

    @classmethod
    async def update(cls, document: model):
        """Update document.
        :param document: document's model to be updated
        :type document: cls.model
        :return: saved document
        :rtype: cls.model
        """
        if hasattr(document, "updated_datetime"):
            document.updated_datetime = datetime.datetime.utcnow()

        return await cls.save(document)

    @classmethod
    async def update_from_schema(cls, document: model, schema: BaseSchema):
        """Update document from schema.
        :param document: document's model to be updated
        :type document: cls.model
        :param schema: schema with document's new data
        :type schema: BaseSchema
        :return: saved document
        :rtype: cls.model
        """
        changes_detected = False
        for name, value in schema.dict(exclude_unset=True).items():
            if hasattr(document, name) and value != getattr(document, name):
                changes_detected = True
                setattr(document, name, value)

        if changes_detected:
            return await cls.update(document)

        return document
