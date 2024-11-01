from typing import Optional
from src.adapters.data_mappers.cliente_entity_data_mapper import ClientEntityDataMapper
from src.adapters.data_mappers.currency_entity_data_mapper import (
    CurrencyEntityDataMapper,
)
from src.adapters.data_mappers.produto_escolhido_entity_data_mapper import (
    ProdutoEscolhidoEntityDataMapper,
)
from src.adapters.driven.infra.models.purchases import Purchase
from src.core.domain.entities.compra_entity import PartialCompraEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.compra_status import CompraStatus


class CompraEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, compra: Purchase):
        return PartialCompraEntity(
            id=compra.id,
            status=CompraStatus(compra.status),
            total=PrecoValueObject(
                value=compra.total_value,
                currency=CurrencyEntityDataMapper.from_db_to_domain(compra.currency),
            ),
            created_at=compra.created_at,
            updated_at=compra.updated_at,
            deleted_at=compra.deleted_at,
            client=(
                ClientEntityDataMapper.from_db_to_domain(compra.client)
                if compra.client
                else None
            ),
            selected_products=(
                [
                    ProdutoEscolhidoEntityDataMapper.from_db_to_domain(selected_product)
                    for selected_product in compra.selected_products
                ]
                if compra.selected_products
                else []
            ),
        )

    @classmethod
    def from_domain_to_db(
        cls, compra: PartialCompraEntity, payment: Optional[PagamentoEntity] = None
    ):
        purchase_selected_products = (
            [
                {
                    "purchase": compra.id,
                    "selected_product": {
                        "id": selected_product.id,
                        "product": selected_product.product.id,
                        "added_components": (
                            [
                                {
                                    "component": comp.id,
                                    "selected_product": selected_product.id,
                                }
                                for comp in selected_product.added_components
                            ]
                            if selected_product.added_components
                            else []
                        ),
                    },
                }
                for selected_product in compra.selected_products
            ]
            if compra.selected_products
            else []
        )

        return {
            "id": compra.id,
            "status": compra.status.value,
            "total_value": compra.total.value,
            "currency": compra.total.currency.id,
            "client": compra.client.id,
            "payment": payment.id if payment else None,
            "purchase_selected_products": purchase_selected_products,
        }
