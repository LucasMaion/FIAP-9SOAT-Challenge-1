from typing import List, Optional
from src.adapters.data_mappers.cliente_entity_data_mapper import ClientEntityDataMapper
from src.adapters.data_mappers.compra_data_mapper import CompraEntityDataMapper
from src.adapters.data_mappers.produto_entity_data_mapper import ProdutoEntityDataMapper
from src.adapters.driven.infra.models.persona import Persona
from src.adapters.driven.infra.models.purchases import Purchase
from src.core.domain.aggregates.cliente_aggregate import ClienteAggregate


class ClienteAggregateDataMapper:
    @classmethod
    def from_db_to_domain(
        cls, client: Persona, purchases: Optional[List[Purchase]] = None
    ):
        return ClienteAggregate(
            orders=(
                [
                    CompraEntityDataMapper.from_db_to_domain(purchase)
                    for purchase in purchases
                ]
                if purchases
                else []
            ),
            client=ClientEntityDataMapper.from_db_to_domain(client),
        )
