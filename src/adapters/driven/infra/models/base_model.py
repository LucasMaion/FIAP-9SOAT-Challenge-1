from datetime import datetime
from peewee import Model, DateTimeField, AutoField
from playhouse.signals import pre_save
from src.adapters.driven.infra import db


class BaseModel(Model):
    """Base model class that all models will inherit from."""

    id = AutoField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    deleted_at = DateTimeField(null=True)

    class Meta:
        database = db

    @classmethod
    def update(cls, *args, **kwargs):
        kwargs["updated_at"] = datetime.now()
        return super(BaseModel, cls).update(*args, **kwargs)

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.deleted_at.is_null())

    @classmethod
    def get(cls, *query, **kwargs):
        query = (cls.deleted_at.is_null(), *query)
        return super().get(*query, **kwargs)


@pre_save(sender=BaseModel)
def apply_default_values(model_class, instance, created):
    if instance.created_at is None:
        instance.created_at = BaseModel._meta.fields["created_at"].default
    if instance.updated_at is None:
        instance.updated_at = BaseModel._meta.fields["updated_at"].default
