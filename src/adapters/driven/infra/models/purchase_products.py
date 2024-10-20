from peewee import ForeignKeyField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.products import Product
from src.adapters.driven.infra.models.purchases import Purchase


class PurchaseProduct(BaseModel):
    class Meta:
        db_table = "purchase_product"

    product = ForeignKeyField(Product, backref="purchase_products")
    purchase = ForeignKeyField(Purchase, backref="purchase_products")
