from peewee import CharField, ForeignKeyField, DateTimeField

from src.adapters.driven.infra.models.address import Address
from src.adapters.driven.infra.models.base_model import BaseModel


class Persona(BaseModel):
    name = CharField()
    document = CharField(null=True, unique=True)
    email = CharField(null=True)
    phone = CharField(null=True)
    birth_date = DateTimeField(null=True)
    address = ForeignKeyField(Address, backref="personas", null=True, unique=True)
