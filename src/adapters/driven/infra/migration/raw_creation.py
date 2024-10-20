from src.adapters.driven.infra import db
from src.adapters.driven.infra.models.categories import Category
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payment_methods import PaymentMethod
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.models.product_components import ProductComponent
from src.adapters.driven.infra.models.products import Product
from src.adapters.driven.infra.models.purchase_products import PurchaseProduct
from src.adapters.driven.infra.models.purchases import Purchase


def create_tables():
    db.create_tables(
        [
            Category,
            Currency,
            Product,
            ProductComponent,
            Purchase,
            PurchaseProduct,
            PaymentMethod,
            Payment,
        ]
    )
