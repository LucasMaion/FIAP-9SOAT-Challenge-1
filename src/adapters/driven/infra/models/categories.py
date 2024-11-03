from peewee import CharField, BooleanField

from src.adapters.driven.infra.models.base_model import BaseModel


class Category(BaseModel):
    name = CharField()
    description = CharField(null=True)
    is_component = BooleanField(default=False)
