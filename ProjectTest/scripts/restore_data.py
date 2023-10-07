#!/bin/python
"""
¡¡¡ DANGER !!!
Restore basic data into DB instance.
"""
import asyncio
import sys

# Manually append path for import reference
sys.path.append("/app")

from app.core.config import settings
from app.database.database import init_database
from app.models.user import User

CLEAR_COLLECTIONS = []

DATA = {}


async def clear_existing_data():
    """Drop existing collections."""
    for model_dao in CLEAR_COLLECTIONS:
        collection = database.metadata.get_collection(model_dao.model)
        await collection.drop()


async def insert_data():
    """Insert new data into database."""
    # Dummy user
    admin_user = User(
        username="admin",
        password="1234",
        email="admin@admin.com",
    )
    await admin_user.save()

    # Data bulk
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
             "are you sure to continue? ").lower() not in ["y", "yes"]:
        exit(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_database())
    loop.run_until_complete(clear_existing_data())
    loop.run_until_complete(insert_data())
