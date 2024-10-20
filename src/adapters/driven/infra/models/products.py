from peewee import CharField, FloatField, ForeignKeyField, BooleanField
from playhouse.signals import pre_save

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.categories import Category
from src.adapters.driven.infra.models.currencies import Currency


class Product(BaseModel):
    name = CharField()
    category = ForeignKeyField(Category, backref="products", null=True)
    price = FloatField(null=True)
    currency = ForeignKeyField(Currency, backref="products", null=True)
    allow_components = BooleanField(default=False)
    is_active = BooleanField(default=False)


@pre_save(sender=Product)
def apply_default_values(model_class, instance, created):
    if instance.allow_components is None:
        instance.allow_components = Product._meta.fields["allow_components"].default
    if instance.is_active is None:
        instance.is_active = Product._meta.fields["is_active"].default
