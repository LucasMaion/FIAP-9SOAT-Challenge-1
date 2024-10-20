from abc import ABC, abstractmethod
from typing import Any

from src.core.domain.aggregates.client_aggregate import ClientAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.cliente_entity import ClientEntity, PartialClientEntity
from src.core.helpers.options.client_find_options import ClientFindOptions


class ClientRepository(Repository, ABC):
    @abstractmethod
    def create(self, produto: PartialClientEntity) -> ClientAggregate:
        raise NotImplementedError()

    @abstractmethod
    def update(self, produto: ClientEntity) -> ClientAggregate:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, produto_id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_by_purchase_id(self, produto_id: int) -> ClientAggregate:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: ClientFindOptions) -> list[ClientAggregate]:
        raise NotImplementedError()
