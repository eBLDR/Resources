"""
CRUD transactions handler.
"""
import csv
import json
from io import StringIO
from typing import List, Union

from bson.objectid import ObjectId
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from odmantic import Model

from app.api.param_validator import FileFormats
from helpers import util_serializer
from helpers.util_exception import BaseCustomException


async def _save(
        input_schema,
        get_schema,
        resource_dao,
        document=False):
    try:
        return await get_schema.from_document(
            await (
                resource_dao.update_from_schema(
                    document,
                    input_schema,
                )
                if document else resource_dao.save_from_schema(input_schema)
            ),
        )
    except BaseCustomException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.msg,
        )


async def create(
        post_schema,
        get_schema,
        resource_dao,
        assert_unique_id=True,
):
    """Create document from schema managing validations.
    :param post_schema: post schema
    :type post_schema: BaseSchema
    :param get_schema: get schema
    :type get_schema: BaseSchema
    :param resource_dao: resource DAO
    :type resource_dao: BaseDAO
    :param assert_unique_id: True to assert id uniqueness
    :type assert_unique_id: bool
    :return: get schema
    :rtype: BaseSchema
    """
    if assert_unique_id:
        await assert_uniqueness(resource_dao, post_schema.id)

    return await _save(
        post_schema,
        get_schema,
        resource_dao,
    )


async def update(
        document_id,
        patch_schema,
        get_schema,
        resource_dao,
):
    """Update document from schema managing validations.
    :param document_id: document id
    :type document_id: str
    :param patch_schema: patch schema
    :type patch_schema: BaseSchema
    :param get_schema: get schema
    :type get_schema: BaseSchema
    :param resource_dao: resource DAO
    :type resource_dao: BaseDAO
    :return: get schema
    :rtype: BaseSchema
    """
    document = await read_one_document_by_id(resource_dao, document_id)
    return await _save(
        patch_schema,
        get_schema,
        resource_dao,
        document=document,
    )


async def _read(method, **method_kwargs):
    """Read document(s), raise HTTP 404 if no result is found.
    :param method: callable method
    :type method: method
    :return: document(s) found
    :rtype: Union[Model, List[Model]]
    """
    result = await method(**method_kwargs)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


async def read_one_document_by_id(
        document_dao,
        document_id: Union[ObjectId, str, int],
):
    """Read document.
    :param document_dao: document's DAO
    :type document_dao: BaseDAO
    :param document_id: document id
    :type document_id: Union[ObjectId, str, int]
    :return: document found
    :rtype: document_dao.model
    """
    method = document_dao.find_one_by_id
    return await _read(method, document_id=document_id)


async def read_all_documents(document_dao, method=None, **method_kwargs):
    """Read all documents.
    :param document_dao: document's DAO
    :type document_dao: BaseDAO
    :param method: DAO's callable method
    :type method: method
    :return: documents found
    :rtype: List[document_dao.model]
    """
    if not method:
        method = document_dao.find
        method_kwargs = {}
    return await _read(method, **method_kwargs)


async def assert_uniqueness(
        document_dao,
        document_id: Union[ObjectId, str, int],
):
    """Read document, raise HTTP 409 if result is found.
    :param document_dao: document's DAO
    :type document_dao: BaseDAO
    :param document_id: document id
    :type document_id: Union[ObjectId, str, int]
    :return: bool
    :rtype: bool
    """
    if await document_dao.find_one_by_id(document_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicated id: {document_id}",
        )

    return True


def generate_file_response(
        file_content_data: Union[dict, List[dict]],
        file_format: str,
        file_name: str,
) -> StreamingResponse:
    """Generate file response.
    :param file_content_data: file content
    :type file_content_data: Union[dict, list[dict]]
    :param file_format: file's format
    :type file_format: str
    :param file_name: file's name
    :type file_name: str
    :return: file response
    :rtype: StreamingResponse
    """
    if file_format == FileFormats.json:
        file = convert_data_to_json_file(file_content_data)
    elif file_format == FileFormats.csv:
        file = convert_data_to_csv_file(file_content_data)
    else:
        file = StringIO()

    return StreamingResponse(
        content=iter(file.getvalue()),
        media_type=f"text/{file_format}",
        headers={
            "Content-Disposition": f"attachment; filename={file_name}"f".{file_format}",
        },
    )


def convert_data_to_json_file(
        file_content_data: Union[dict, List[dict]],
) -> StringIO:
    """Convert data to JSON file.
    :param file_content_data: file content data
    :type file_content_data: Union[dict, list[dict]]
    :return: file
    :rtype: StringIO
    """
    file = StringIO()
    json.dump(
        file_content_data,
        file,
        default=util_serializer.fallback_default_serializer,
    )

    return file


def convert_data_to_csv_file(
        file_content_data: Union[dict, List[dict]],
) -> StringIO:
    """Convert data to CSV file.
    :param file_content_data: file content data
    :type file_content_data: Union[dict, list[dict]]
    :return: file
    :rtype: StringIO
    """
    if not isinstance(file_content_data, list):
        file_content_data = [file_content_data]

    headers = set()
    for row_data in file_content_data:
        headers.update(list(row_data.keys()))

    file = StringIO()
    w = csv.DictWriter(file, fieldnames=sorted(list(headers)))
    w.writeheader()

    for row_data in file_content_data:
        w.writerow(row_data)

    return file
