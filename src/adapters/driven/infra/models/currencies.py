from peewee import CharField, BooleanField

from src.adapters.driven.infra.models.base_model import BaseModel


class Currency(BaseModel):
    symbol = CharField()
    name = CharField()
    code = CharField()
    is_active = BooleanField(default=True)
