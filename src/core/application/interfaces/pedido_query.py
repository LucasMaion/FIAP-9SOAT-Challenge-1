from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.application.ports.pedido_query import PedidoQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


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
        self, options: Optional[ProdutoFindOptions] = None
    ) -> List[PedidoAggregate]:
        raise NotImplementedError()
