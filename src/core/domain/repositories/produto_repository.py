from abc import ABC, abstractmethod
from typing import Any

from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class ProdutoRepository(Repository, ABC):

    @abstractmethod
    def create(self, produto: PartialProdutoEntity) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def update(self, produto: ProdutoEntity) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, produto_id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_by_product_id(self, produto_id: int) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: ProdutoFindOptions) -> list[ProdutoAggregate]:
        raise NotImplementedError()
