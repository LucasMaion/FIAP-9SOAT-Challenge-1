from abc import ABC, abstractmethod
from typing import Any

from src.core.domain.aggregates.cliente_aggregate import ClienteAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.cliente_entity import ClienteEntity, PartialClienteEntity
from src.core.helpers.options.client_find_options import ClientFindOptions


class ClienteRepository(Repository, ABC):
    @abstractmethod
    def create(self, produto: PartialClienteEntity) -> ClienteAggregate:
        raise NotImplementedError()

    @abstractmethod
    def update(self, produto: ClienteEntity) -> ClienteAggregate:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, produto_id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_by_purchase_id(self, produto_id: int) -> ClienteAggregate:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: ClientFindOptions) -> list[ClienteAggregate]:
        raise NotImplementedError()
