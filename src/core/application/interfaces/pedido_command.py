from abc import ABC, abstractmethod

from src.core.application.ports.pedido_query import PedidoQuery
from src.core.application.ports.produto_query import ProdutoQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.compra_entity import PartialCompraEntity
from src.core.domain.repositories.pedido_repository import PedidoRepository
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.interfaces.chace_service import CacheService


class IPedidoCommand(ABC):
    def __init__(
        self,
        purchase_repository: PedidoRepository,
        purchase_query: PedidoQuery,
        produto_query: ProdutoQuery,
        cache_service=CacheService,
    ):
        self.purchase_repository = purchase_repository
        self.purchase_query = purchase_query
        self.produto_query = produto_query
        self.cache_service = cache_service

    @abstractmethod
    def create_pedido(self, pedido: PartialCompraEntity) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def concludes_pedido(self, pedido_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def cancel_pedido(self, pedido_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def add_new_product(self, pedido_id: int, product_id: int):
        raise NotImplementedError()

    @abstractmethod
    def remove_select_product(self, pedido_id: int, selected_product_id: int):
        raise NotImplementedError()

    @abstractmethod
    def add_component_to_select_product(
        self, pedido_id: int, selected_product_id: int, component_id: int
    ):
        raise NotImplementedError()

    @abstractmethod
    def update_status(
        self, pedido_id: int, new_status: CompraStatus
    ) -> PedidoAggregate:
        raise NotImplementedError()
