from typing import Any

from src.adapters.driven.infra.repositories.orm_repository import OrmRepository
from src.core.domain.aggregates.client_aggregate import ClientAggregate
from src.core.domain.entities.cliente_entity import ClientEntity, PartialClientEntity
from src.core.domain.repositories.client_repository import ClientRepository
from src.core.helpers.options.client_find_options import ClientFindOptions


class OrmClientRepository(OrmRepository, ClientRepository):
    def __init__(self, session: Any):
        self.session = session

    def create(self, produto: PartialClientEntity) -> ClientAggregate:
        raise NotImplementedError()

    def update(self, produto: ClientEntity) -> ClientAggregate:
        raise NotImplementedError()

    def delete(self, produto_id: int):
        raise NotImplementedError()

    def get_by_purchase_id(self, produto_id: int) -> ClientAggregate:
        raise NotImplementedError()

    def find(self, query_options: ClientFindOptions) -> list[ClientAggregate]:
        raise NotImplementedError()
