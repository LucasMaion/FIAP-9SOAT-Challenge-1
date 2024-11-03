from typing import List, Optional
from src.core.application.interfaces.pedido_query import IPedidoQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class PedidoServiceQuery(IPedidoQuery):

    def get(self, pedido_id: int) -> PedidoAggregate:
        result = self.purchase_query.get(pedido_id)
        return result or None

    def index(
        self, options: Optional[PedidoFindOptions] = None
    ) -> List[PedidoAggregate]:
        if not options:
            return self.purchase_query.get_all()
        result = self.purchase_query.find(options)
        return result or None
