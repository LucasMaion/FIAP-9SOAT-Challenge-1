from typing import Any

from src.adapters.driven.infra.repositories.orm_repository import OrmRepository
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.repositories.pedido_repository import PedidoRepository
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class OrmPedidoRepository(OrmRepository, PedidoRepository):
    def __init__(self, session: Any):
        self.session = session

    def create(self, produto: PartialCompraEntity) -> PedidoAggregate:
        raise NotImplementedError()

    def update(self, produto: CompraEntity) -> PedidoAggregate:
        raise NotImplementedError()

    def delete(self, produto_id: int):
        raise NotImplementedError()

    def get_by_purchase_id(self, produto_id: int) -> PedidoAggregate:
        raise NotImplementedError()

    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        raise NotImplementedError()
