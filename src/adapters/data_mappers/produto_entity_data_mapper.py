from decimal import Decimal
from src.adapters.driven.infra.models.products import Product
from src.core.domain.entities.produto_entity import PartialProdutoEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.adapters.data_mappers.currency_entity_data_mapper import (
    CurrencyEntityDataMapper,
)
from src.adapters.data_mappers.categoria_entity_data_mapper import (
    CategoriaEntityDataMapper,
)


class ProdutoEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, produto: Product):
        return PartialProdutoEntity(
            id=produto.id,
            name=produto.name,
            price=(
                PrecoValueObject(
                    value=round(Decimal(produto.price), 2),
                    currency=CurrencyEntityDataMapper.from_db_to_domain(
                        produto.currency
                    ),
                )
                if produto.price
                else None
            ),
            category=(
                CategoriaEntityDataMapper.from_db_to_domain(produto.category)
                if produto.category
                else None
            ),
            created_at=produto.created_at,
            updated_at=produto.updated_at,
            deleted_at=produto.deleted_at,
            allow_components=produto.allow_components,
            is_active=produto.is_active,
            components=(
                [cls.from_db_to_domain(comp.component) for comp in produto.components]
                if hasattr(produto, "components") and produto.components is not None
                else None
            ),
        )

    @classmethod
    def from_domain_to_db(cls, produto: PartialProdutoEntity):
        return {
            "id": produto.id,
            "name": produto.name,
            "price": produto.price.value if produto.price else None,
            "allow_components": produto.allow_components,
            "is_active": produto.is_active,
            "category": produto.category.id if produto.category else None,
            "currency": produto.price.currency.id if produto.price else None,
            "components": (
                [
                    {"product": produto.id, "component": comp.id}
                    for comp in produto.components
                ]
                if produto.components
                else None
            ),
        }
