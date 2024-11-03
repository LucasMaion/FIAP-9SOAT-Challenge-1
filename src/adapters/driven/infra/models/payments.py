from peewee import FloatField, ForeignKeyField, IntegerField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payment_methods import PaymentMethod


class Payment(BaseModel):
    payment_method = ForeignKeyField(PaymentMethod, backref="payments")
    currency = ForeignKeyField(Currency, backref="payments")
    value = FloatField()
    status = IntegerField()
