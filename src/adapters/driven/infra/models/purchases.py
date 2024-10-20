from peewee import CharField, FloatField, BooleanField

from src.adapters.driven.infra.models.base_model import BaseModel


class Purchase(BaseModel):
    status = CharField()
    total_value = FloatField(default=0)
    finalized = BooleanField(default=False)
    canceled = BooleanField(default=False)
