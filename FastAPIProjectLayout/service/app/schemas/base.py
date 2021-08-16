"""
Base schema management.
"""
from typing import List

from odmantic import Model
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base schema."""

    @classmethod
    async def from_document(cls, document: Model):
        """
        Factory method to instantiate schema from model.
        :param document: model
        :type document: Model
        :return: populated schema
        :rtype: BaseSchema
        """
        schema = cls(**document.dict())
        await cls.populate_references(schema)
        return schema

    @classmethod
    async def from_document_array(cls, documents: List[Model]):
        """
        Factory method to instantiate schema from model array.
        :param documents: model array
        :type documents: List[Model]
        :return: populated schema
        :rtype: BaseSchema
        """
        return [await cls.from_document(document) for document in documents]

    def to_document(self, model):
        """Generate model document from schema.
        :param model: model
        :type model: Model
        :return: populated model
        :rtype: Model
        """
        return model(**self.dict())

    async def populate_references(self):
        """Populate schema references to other documents.
        To be declared by child class."""
