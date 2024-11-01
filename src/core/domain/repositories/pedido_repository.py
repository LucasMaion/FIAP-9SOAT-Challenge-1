from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.entities.pagamento_entity import (
    PagamentoEntity,
    PartialPagamentoEntity,
)
from src.core.helpers.interfaces.chace_service import CacheService
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class PedidoRepository(Repository, ABC):

    def __init__(self, cache_service: CacheService):
        super().__init__()
        self.cache_service = cache_service

    @abstractmethod
    def create(self, pedido: PartialCompraEntity) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def update(
        self, pedido: CompraEntity, payment: Optional[PagamentoEntity] = None
    ) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, pedido_id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_by_purchase_id(self, pedido_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        raise NotImplementedError()
