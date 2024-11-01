from peewee import CharField, BooleanField

from src.adapters.driven.infra.models.base_model import BaseModel


class PaymentMethod(BaseModel):
    class Meta:
        db_table = "payment_method"

    name = CharField()
    sys_name = CharField()
    description = CharField(null=True)
    is_active = BooleanField(default=True)
