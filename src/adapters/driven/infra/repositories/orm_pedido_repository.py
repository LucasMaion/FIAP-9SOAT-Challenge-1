from datetime import datetime
from typing import List, Optional, Union
from src.adapters.data_mappers.compra_data_mapper import CompraEntityDataMapper
from src.adapters.data_mappers.pagamento_data_mapper import PagamentoEntityDataMapper
from src.adapters.data_mappers.pedido_aggregate_data_mapper import (
    PedidoAggregateDataMapper,
)
from src.adapters.driven.infra.models.payments import Payment
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
from src.core.domain.entities.pagamento_entity import PagamentoEntity
from src.core.domain.repositories.pedido_repository import PedidoRepository
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class OrmPedidoRepository(OrmRepository, PedidoRepository):

    def create(self, pedido: PartialCompraEntity) -> PedidoAggregate:
        db_item = CompraEntityDataMapper.from_domain_to_db(pedido)
        purchase_selected_products = db_item.pop("purchase_selected_products", [])
        purchase: Purchase = Purchase.create(**db_item)
        purchase.save()
        self._create_purchase_selected_products(purchase.id, purchase_selected_products)
        purchase = Purchase.get(Purchase.id == purchase.id)
        pedido_aggregate = PedidoAggregateDataMapper.from_db_to_domain(purchase)
        self.cache_service.set(pedido_aggregate.purchase.id, pedido_aggregate)
        return PedidoAggregateDataMapper.from_db_to_domain(purchase)

    def update(
        self, pedido: CompraEntity, payment: Optional[PagamentoEntity] = None
    ) -> PedidoAggregate:
        db_item = CompraEntityDataMapper.from_domain_to_db(pedido, payment)
        purchase_selected_products = db_item.pop("purchase_selected_products", [])
        current_purchase: Union[PedidoAggregate, None] = self.cache_service.get(
            pedido.id
        )
        current_selected_products: List[int] = []
        if current_purchase:
            current_selected_products = [
                sp.id for sp in current_purchase.purchase.selected_products
            ]
        else:
            current_selected_products = [
                sp.product.id
                for sp in PurchaseSelectedProducts.select().where(
                    PurchaseSelectedProducts.purchase == pedido.id
                )
            ]
        selected_product_ids = [
            sp["selected_product"]["id"] for sp in purchase_selected_products
        ]
        selected_products_to_delete = [
            csp for csp in current_selected_products if csp not in selected_product_ids
        ]
        new_selected_products = [
            sp
            for sp in purchase_selected_products
            if sp["selected_product"]["id"] not in current_selected_products
        ]
        update_query: Purchase = Purchase.update(**db_item).where(
            Purchase.id == db_item["id"]
        )
        update_query.execute()
        if selected_products_to_delete:
            PurchaseSelectedProducts.delete().where(
                PurchaseSelectedProducts.purchase << selected_products_to_delete
            ).execute()
        self._create_purchase_selected_products(pedido.id, new_selected_products)
        pedido_aggregate = PedidoAggregateDataMapper.from_db_to_domain(
            Purchase.get(Purchase.id == db_item["id"])
        )
        self.cache_service.set(pedido_aggregate.purchase.id, pedido_aggregate)
        return pedido_aggregate

    def delete(self, pedido_id: int):
        update_query: Purchase = Purchase.update(deleted_at=datetime.now()).where(
            Purchase.id == pedido_id
        )
        update_query.execute()

    def get_by_purchase_id(self, pedido_id: int) -> PedidoAggregate:
        pedido = self.cache_service.get(pedido_id) or OrmPedidoQuery().get(pedido_id)
        return pedido

    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        return OrmPedidoQuery().find(query_options)

    def _create_purchase_selected_products(
        self, purchase_id: int, purchase_selected_products: List[dict]
    ):
        for selected_product in purchase_selected_products:
            selected_product_data = selected_product["selected_product"]
            new_selected_product = SelectedProduct.create(
                product=selected_product_data["product"]
            )
            for component in selected_product_data["added_components"]:
                SelectedProductComponent.create(
                    component=component["component"],
                    selected_product=selected_product_data["product"],
                )
            PurchaseSelectedProducts.create(
                purchase=purchase_id,
                product=new_selected_product.id,
            )
