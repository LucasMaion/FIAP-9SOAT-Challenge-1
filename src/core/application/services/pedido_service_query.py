from typing import List, Optional
from src.core.application.interfaces.pedido_query import IPedidoQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class PedidoServiceQuery(IPedidoQuery):

    def get(self, pedido_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    def index(
        self, options: Optional[PedidoFindOptions] = None
    ) -> List[PedidoAggregate]:
        result = self.purchase_query.find(options)
        return result or None
