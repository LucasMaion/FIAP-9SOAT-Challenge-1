from abc import ABC, abstractmethod

from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.produto_entity import ProdutoEntity
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class ProdutoQuery(ABC):
    @abstractmethod
    def get_only_entity(self, item_id: int) -> ProdutoEntity:
        raise NotImplementedError()

    @abstractmethod
    def get(self, item_id: int) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[ProdutoAggregate]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: ProdutoFindOptions) -> list[ProdutoAggregate]:
        raise NotImplementedError()
