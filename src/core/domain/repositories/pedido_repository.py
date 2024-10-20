from abc import ABC, abstractmethod
from typing import Any

from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class PedidoRepository(Repository, ABC):

    @abstractmethod
    def create(self, produto: PartialCompraEntity) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def update(self, produto: CompraEntity) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, produto_id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_by_purchase_id(self, produto_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        raise NotImplementedError()
