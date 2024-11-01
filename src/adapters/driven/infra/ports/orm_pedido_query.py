from peewee import JOIN
from src.adapters.data_mappers.pedido_aggregate_data_mapper import (
    PedidoAggregateDataMapper,
)
from src.adapters.driven.infra.models.categories import Category
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.models.persona import Persona
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.purchases import Purchase
from src.adapters.driven.infra.models.select_product import SelectedProduct
from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)
from src.core.application.ports.pedido_query import PedidoQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class OrmPedidoQuery(PedidoQuery):
    def get(self, item_id: int) -> PedidoAggregate:
        product: Purchase = Purchase.select().where(Purchase.id == item_id)
        parsed_result = [
            PedidoAggregateDataMapper.from_db_to_domain(res) for res in product
        ]
        if len(parsed_result) == 1:
            return parsed_result[0]
        return None

    def get_all(self) -> list[PedidoAggregate]:
        result: Purchase = (
            Purchase.select()
            .join(
                Currency,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Purchase)
            .join(
                Persona,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Purchase)
            .join(
                Payment,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Purchase)
            .join(
                PurchaseSelectedProducts,
                on=(PurchaseSelectedProducts.purchase == Purchase.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .join(
                SelectedProduct,
                on=(SelectedProduct.product == PurchaseSelectedProducts.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .join(
                SelectedProductComponent,
                on=(SelectedProductComponent.selected_product == SelectedProduct.id),
                join_type=JOIN.LEFT_OUTER,
            )
        )
        parsed_result = [
            PedidoAggregateDataMapper.from_db_to_domain(res) for res in result
        ]
        return parsed_result

    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        queries = []
        if query_options.status:
            status = [status.value for status in query_options.status]
            queries.append(Purchase.status << status)
        if query_options.total_value_range:
            queries.append(
                Purchase.total_value.between(*query_options.total_value_range)
            )

        result: Purchase = (
            Purchase.select()
            .join(
                Currency,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Purchase)
            .join(
                Persona,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Purchase)
            .join(
                Payment,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Purchase)
            .join(
                PurchaseSelectedProducts,
                on=(PurchaseSelectedProducts.purchase == Purchase.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .join(
                SelectedProduct,
                on=(SelectedProduct.product == PurchaseSelectedProducts.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .join(
                SelectedProductComponent,
                on=(SelectedProductComponent.selected_product == SelectedProduct.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .where(*queries)
        )
        parsed_result = [
            PedidoAggregateDataMapper.from_db_to_domain(res) for res in result
        ]
        return parsed_result
