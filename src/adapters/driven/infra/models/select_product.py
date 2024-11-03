from peewee import ForeignKeyField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.products import Product


class SelectedProduct(BaseModel):
    class Meta:
        db_table = "selected_product"

    product = ForeignKeyField(Product, backref="selected_product")
