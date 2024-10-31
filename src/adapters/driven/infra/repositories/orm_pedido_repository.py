from datetime import datetime
from typing import List
from src.adapters.data_mappers.compra_data_mapper import CompraEntityDataMapper
from src.adapters.data_mappers.pedido_aggregate_data_mapper import (
    PedidoAggregateDataMapper,
)
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.purchases import Purchase
from src.adapters.driven.infra.models.select_product import SelectedProduct
from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)
from src.adapters.driven.infra.ports.orm_pedido_query import OrmPedidoQuery
from src.adapters.driven.infra.repositories.orm_repository import OrmRepository
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.entities.pagamento_entity import PartialPagamentoEntity
from src.core.domain.repositories.pedido_repository import PedidoRepository
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class OrmPedidoRepository(OrmRepository, PedidoRepository):

    def create_compra(self, pedido: PartialCompraEntity) -> PedidoAggregate:
        db_item = CompraEntityDataMapper.from_domain_to_db(pedido)
        purchase_selected_products = db_item.pop("purchase_selected_products", [])
        purchase: Purchase = Purchase.create(**db_item)
        purchase.save()
        self._create_purchase_selected_products(purchase.id, purchase_selected_products)
        purchase = Purchase.get(Purchase.id == purchase.id)
        return PedidoAggregateDataMapper.from_db_to_domain(purchase)

    def create_payment(self, payment: PartialPagamentoEntity) -> PedidoAggregate:
        # TODO
        raise NotImplementedError()

    def update_compra(self, pedido: CompraEntity) -> PedidoAggregate:
        db_item = CompraEntityDataMapper.from_domain_to_db(pedido)
        purchase_selected_products = db_item.pop("purchase_selected_products", [])
        current_selected_products: List[
            PurchaseSelectedProducts
        ] = PurchaseSelectedProducts.select().where(
            PurchaseSelectedProducts.purchase == pedido.id
        )
        selected_product_ids = [
            sp["selected_product"]["id"] for sp in purchase_selected_products
        ]
        selected_products_to_delete = [
            csp
            for csp in current_selected_products
            if csp.product.id not in selected_product_ids
        ]
        update_query: Purchase = Purchase.update(**db_item).where(
            Purchase.id == db_item["id"]
        )
        update_query.execute()
        if selected_products_to_delete:
            PurchaseSelectedProducts.delete().where(
                PurchaseSelectedProducts.purchase << selected_products_to_delete
            ).execute()
        self._create_purchase_selected_products(pedido.id, purchase_selected_products)

        return PedidoAggregateDataMapper.from_db_to_domain(
            Purchase.get(Purchase.id == db_item["id"])
        )

    def delete(self, pedido_id: int):
        update_query: Purchase = Purchase.update(deleted_at=datetime.now()).where(
            Purchase.id == pedido_id
        )
        update_query.execute()

    def get_by_purchase_id(self, pedido_id: int) -> PedidoAggregate:
        return OrmPedidoQuery().get(pedido_id)

    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        return OrmPedidoQuery().find(query_options)

    def _create_purchase_selected_products(
        self, purchase_id: int, purchase_selected_products: List[dict]
    ):
        for selected_product in purchase_selected_products:
            selected_product_data = selected_product["selected_product"]
            new_selected_product = SelectedProduct.get_or_create(
                product=selected_product_data["product"]
            )[0]
            for component in selected_product_data["added_components"]:
                SelectedProductComponent.get_or_create(
                    component=component["component"],
                    product=selected_product_data["product"],
                )
            PurchaseSelectedProducts.get_or_create(
                purchase=purchase_id,
                product=new_selected_product.id,
            )
