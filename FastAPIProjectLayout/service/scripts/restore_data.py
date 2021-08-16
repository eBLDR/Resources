#!/bin/python
"""
¡¡¡ DANGER !!!
Restore basic data into MongoDB instance.
"""
import asyncio
import sys

# Manually append path for import reference
sys.path.append("/app")

from app.core.config import settings
from app.database.engine import close_connection, open_connection, db

CLEAR_COLLECTIONS = []

DATA = {}


async def clear_existing_data():
    """Drop existing collections."""
    for model_dao in CLEAR_COLLECTIONS:
        collection = db.engine.get_collection(model_dao.model)
        await collection.drop()


async def insert_data():
    """Insert new documents into collections."""
    for model_dao, documents_data in DATA.items():
        for document_data in documents_data:
            document = model_dao.model(**document_data)
            await model_dao.save(document)

    print("Created...")


if __name__ == '__main__':
    if settings.ENVIRONMENT != "local":
        print("¡¡APP is not running in local environment!!\nScript only available in local.")
        exit(1)

    if input("ALL data will be deleted and restored with fresh one, "
             "are you sure to continue? ") not in ["Y", "y"]:
        exit(1)

    loop = asyncio.get_event_loop()
    open_connection()
    loop.run_until_complete(clear_existing_data())
    loop.run_until_complete(insert_data())
    close_connection()
