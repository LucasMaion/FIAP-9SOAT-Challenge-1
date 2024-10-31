from peewee import CharField
from src.adapters.driven.infra.models.base_model import BaseModel


class Address(BaseModel):
    zip_code = CharField(null=True)
    street = CharField(null=True)
    number = CharField(null=True)
    city = CharField(null=True)
    state = CharField(null=True)
    country = CharField(null=True)
    additional_information = CharField(null=True)
