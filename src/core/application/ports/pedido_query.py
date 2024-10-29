from abc import ABC, abstractmethod

from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class PedidoQuery(ABC):
    @abstractmethod
    def get(self, item_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[PedidoAggregate]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        raise NotImplementedError()
