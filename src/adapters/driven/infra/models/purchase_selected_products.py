from peewee import ForeignKeyField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.purchases import Purchase
from src.adapters.driven.infra.models.select_product import SelectedProduct


class PurchaseSelectedProducts(BaseModel):
    class Meta:
        db_table = "purchase_selected_product"
        # indexes = ((("selected_products", "purchase"), True),)

    product = ForeignKeyField(SelectedProduct, backref="purchases")
    purchase = ForeignKeyField(Purchase, backref="selected_products")
