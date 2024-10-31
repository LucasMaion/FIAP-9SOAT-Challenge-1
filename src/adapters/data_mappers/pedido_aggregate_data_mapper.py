from src.adapters.data_mappers.compra_data_mapper import CompraEntityDataMapper
from src.adapters.data_mappers.pagamento_data_mapper import PagamentoEntityDataMapper
from src.adapters.driven.infra.models.purchases import Purchase
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate


class PedidoAggregateDataMapper:
    @classmethod
    def from_db_to_domain(cls, purchase: Purchase):
        return PedidoAggregate(
            purchase=CompraEntityDataMapper.from_db_to_domain(purchase),
            payment=(
                PagamentoEntityDataMapper.from_db_to_domain(purchase.payment)
                if purchase.payment
                else None
            ),
        )
