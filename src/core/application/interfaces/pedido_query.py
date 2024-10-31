from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.application.ports.pedido_query import PedidoQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class IPedidoQuery(ABC):
    def __init__(
        self,
        purchase_query: PedidoQuery,
    ):
        self.purchase_query = purchase_query

    @abstractmethod
    def get(self, pedido_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def index(
        self, options: Optional[PedidoFindOptions] = None
    ) -> List[PedidoAggregate]:
        raise NotImplementedError()
