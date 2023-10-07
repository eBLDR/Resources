"""
CRUD transactions' handler.
"""
from typing import List, Union

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.base_model import BaseModel


async def _save(
        model: BaseModel,
        update_flag: bool = False,
        update_data: BaseModel = None,
) -> BaseModel:
    """Persist entry, raise HTTP 409 if inconsistent data is provided.
    :param model: entry model
    :type model: BaseModel
    :param update_flag: flag for update
    :type update_flag: bool
    :param update_data: model containing new data for update
    :type update_data: BaseModel
    :return: persisted model
    :rtype: BaseModel
    """
    try:
        if update_flag:
            return await model.update(update_data)
        else:
            return await model.save()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicated key violation",
        )


async def create(model: BaseModel) -> BaseModel:
    """Create new entry from model.
    :param model: entry model
    :type model: BaseModel
    :return: created model
    :rtype: BaseModel
    """
    return await _save(model)


async def update_by_id(id_: int, new_model_data: BaseModel) -> BaseModel:
    """Update entry from model.
    :param id_: entry's id
    :type id_: int
    :param new_model_data: entry model containing new data
    :type new_model_data: BaseModel
    :return: updated model
    :rtype: BaseModel
    """
    if existing_model := await read_one_by_id(new_model_data, id_):
        return await _save(existing_model, update_flag=True, update_data=new_model_data)


async def _read(method, **method_kwargs):
    """Read record(s), raise HTTP 404 if no result is found.
    :param method: callable method
    :type method: method
    :return: record(s) found
    :rtype: Union[Model, List[Model]]
    """
    result = await method(**method_kwargs)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


async def read_one_by_id(model, id_: int):
    """Read one entry by id.
    :param model: entry model
    :type model: BaseModel
    :param id_: entry id
    :type id_: int
    :return: found entry, if any
    :rtype: BaseModel
    """
    method = model.find_one_by_id
    return await _read(method, id_=id_)


async def read_all(model, method=None, **method_kwargs):
    """Read all entries.
    :param model: entry model
    :type model: BaseModel
    :param method: model's callable method
    :type method: method
    :return: found entries, if any
    :rtype: List[BaseModel]
    """
    if not method:
        method = model.find_all
        method_kwargs = {}
    return await _read(method, **method_kwargs)


async def delete(model, id_: int):
    """Delete entry by id.
    :param model: entry model
    :type model: BaseModel
    :param id_: entry id
    :type id_: int
    """
    if existing_model := await read_one_by_id(model, id_):
        await existing_model.delete()
        return {"deleted": "OK"}
