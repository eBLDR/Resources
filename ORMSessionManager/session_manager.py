"""
Session manager, CRUD transactions against DB.
"""
from importlib import import_module

from engine import SESSION

PATH_TO_MODELS = 'models'

MODELS = import_module(PATH_TO_MODELS)


def session_manager(table_name, values=None, filters=None, create=False, read=False, update=False, delete=False):
    """
    Manages database connections.
    :param table_name: table's name to be accessed
    :param values: values for record
    :param filter: filters for querying
    :param create: True for create mode
    :param read: True for read mode
    :param update: True for update mode
    :param delete: True for delete mode
    """
    if values:
        validate_data(table_name, values)
    elif filters:
        validate_data(table_name, filters)
    else:
        validate_data(table_name)

    session = SESSION()

    try:
        table = getattr(MODELS, table_name)
        if read:
            buff = session.query(table)
            if filters:
                buff = buff.filter_by(**filters)
            return buff
        if not read:
            if create:
                record = table(**values)
                session.add(record)
            if update or delete:
                buff = session_manager(table_name, filters=filters, read=True).all()
                if update:
                    for record in buff:
                        record.update(values)
                if delete:
                    for record in buff:
                        session.delete(record)
            session.commit()
    except Exception as exc:
        # Log error here
        if not read:
            session.rollback()
        raise exc
    finally:
        session.close()

 
def validate_data(table_name, columns=None):
    """
    Validates data against database.
    :param table_name: table's name
    :param columns: dictionary containing the columns' names
    """
    try:
        if hasattr(MODELS, table_name):
            table = getattr(MODELS, table_name)
        else:
            error_msg = 'Table {} does not exist.'.format(table_name)
            raise AttributeError(error_msg)
        if columns and not all([hasattr(table, column) for column in columns]):
            error_msg = 'Columns {} not found in table {}.'.format([col for col in columns], table_name)
            raise AttributeError(error_msg)
    except Exception as exc:
        # Log error here
        raise exc


# CRUD Transactions
def create(table_name, values):
    """
    Insert a new record into database.
    :param table_name: table's name
    :param values: values of the new object
    """
    session_manager(table_name, values=values, create=True)  


def read(table_name, filters=None):
    """
    Query records from database.
    :param table_name: table's name
    :param filters: filters for query
    :return: fetched data
    """
    return session_manager(table_name, filters=filters, read=True)


def update(table_name, filters, new_values):
    """
    Update an existing record from the database.
    :param table_name: table's name
    :param filters: filters for update
    :param new_values: values to be updated
    """
    session_manager(table_name, filters=filters, values=new_values, update=True)


def delete(table_name, filters):
    """
    Delete an existing record from the database.
    :param table_name: table's name
    :param filters: filters for deletion
    """
    session_manager(table_name, filters=filters, delete=True)
