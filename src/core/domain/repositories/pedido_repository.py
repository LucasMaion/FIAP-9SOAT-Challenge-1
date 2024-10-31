from abc import ABC, abstractmethod

from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.entities.pagamento_entity import PartialPagamentoEntity
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class PedidoRepository(Repository, ABC):

    @abstractmethod
    def create_compra(self, pedido: PartialCompraEntity) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def create_payment(self, payment: PartialPagamentoEntity) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def update_compra(self, pedido: CompraEntity) -> PedidoAggregate:
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
