from peewee import ForeignKeyField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.products import Product
from src.adapters.driven.infra.models.select_product import SelectedProduct


class SelectedProductComponent(BaseModel):
    class Meta:
        db_table = "selected_product_component"
        # indexes = ((("selected_product_component", "added_components"), True),)

    selected_product = ForeignKeyField(SelectedProduct, backref="added_components")
    component = ForeignKeyField(Product, backref="selected_product_component")
