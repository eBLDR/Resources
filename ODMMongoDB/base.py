import datetime
import uuid

from pymodm import MongoModel, fields


def get_random_uuid():
    return uuid.uuid4().hex


class Base(MongoModel):
    uuid = fields.CharField(required=True, default=get_random_uuid)
    created_timestamp = fields.DateTimeField(required=True, default=datetime.datetime.utcnow)
    updated_timestamp = fields.DateTimeField(required=True, default=datetime.datetime.utcnow)
    deleted_timestamp = fields.DateTimeField()

    def save(self):
        super().save()

    def to_dict(self):
        dict_ = self.to_son().to_dict()
        if '_id' in dict_:
            del dict_['_id']
        return dict_


class BaseDAO:
    model = Base

    @classmethod
    def create(cls, save=True, **kwargs):
        for key in list(kwargs.keys()):
            if kwargs[key] is None:
                del kwargs[key]
        if hasattr(cls.model, 'uuid') and not kwargs.get('uuid'):
            kwargs['uuid'] = get_random_uuid()
        document = cls.model(**kwargs)
        if save:
            document.save()
        return document

    @classmethod
    def get(cls, id_):
        return cls.assert_first(
            cls.model.objects.raw(
                {'_id': id_},
            )
        )

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.assert_first(
            cls.model.objects.raw(
                {'uuid': uuid},
            )
        )


    @classmethod
    def get_all(cls):
        return cls.assert_all(
            cls.model.objects
        )


    @classmethod
    def update(cls, id_, data):
        document = cls.get(id_)
        return cls._update(document, data)

    @classmethod
    def update_by_uuid(cls, uuid, data):
        document = cls.get_by_uuid(uuid)
        return cls._update(document, data)

    @classmethod
    def _update(cls, document, data):
        if not data:
            return document
        for attr, new_value in data.items():
            if hasattr(cls.model, attr):
                setattr(document, attr, new_value)
        if hasattr(cls.model, 'updated_timestamp'):
            setattr(document, 'updated_timestamp', datetime.datetime.utcnow())
        document.save()
        return document

    @classmethod
    def delete(cls, id_):
        document = cls.get(id_)
        return cls._delete(document)

    @classmethod
    def delete_by_uuid(cls, uuid):
        document = cls.get_by_uuid(uuid)
        return cls._delete(document)

    @classmethod
    def _delete(cls, document):
        """Not deleting, just setting a flag as deleted."""
        if hasattr(cls.model, 'deleted_timestamp'):
            document.deleted_timestamp = datetime.datetime.utcnow()
            document.save()
        return document

    @classmethod
    def first(cls, filters):
        return cls.assert_first(
            cls.model.objects.raw(filters)
        )

    @classmethod
    def all(cls, filters):
        return cls.assert_all(
            cls.model.objects.raw(filters)
        )

    @staticmethod
    def assert_first(queryset):
        if queryset.count() > 0:
            return queryset.first()

    @staticmethod
    def assert_all(queryset):
        if queryset.count() > 0:
            return list(queryset.all())
        return []
