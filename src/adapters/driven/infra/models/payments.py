from peewee import FloatField, ForeignKeyField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payment_methods import PaymentMethod
from src.adapters.driven.infra.models.purchases import Purchase


class Payment(BaseModel):
    payment_method = ForeignKeyField(PaymentMethod, backref="payments")
    purchase = ForeignKeyField(Purchase, backref="payments")
    currency = ForeignKeyField(Currency, backref="payments")
    value = FloatField()
