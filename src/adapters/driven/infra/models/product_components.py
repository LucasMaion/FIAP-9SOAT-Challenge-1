from peewee import ForeignKeyField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.products import Product


class ProductComponent(BaseModel):
    class Meta:
        db_table = "product_component"
        # indexes = ((("product", "components"), True),)

    product = ForeignKeyField(Product, backref="components")
    component = ForeignKeyField(Product, backref="product")
