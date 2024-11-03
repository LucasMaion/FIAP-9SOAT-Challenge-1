from peewee import FloatField, ForeignKeyField, IntegerField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.models.persona import Persona


class Purchase(BaseModel):
    status = IntegerField()
    total_value = FloatField(default=0)
    currency = ForeignKeyField(Currency, backref="purchase")
    client = ForeignKeyField(Persona, backref="purchases")
    payment = ForeignKeyField(Payment, backref="purchase", null=True, unique=True)
