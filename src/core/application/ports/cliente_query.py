from abc import ABC, abstractmethod

from src.core.domain.aggregates.cliente_aggregate import ClienteAggregate
from src.core.helpers.options.client_find_options import ClientFindOptions


class ClienteQuery(ABC):
    @abstractmethod
    def get(self, item_id: int) -> ClienteAggregate:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[ClienteAggregate]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: ClientFindOptions) -> list[ClienteAggregate]:
        raise NotImplementedError()
