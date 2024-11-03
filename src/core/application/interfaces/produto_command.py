from abc import ABC, abstractmethod

from src.core.application.ports.categoria_query import CategoriaQuery
from src.core.application.ports.currency_query import CurrencyQuery
from src.core.application.ports.produto_query import ProdutoQuery
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.domain.repositories.produto_repository import ProdutoRepository


class IProductCommand(ABC):

    def __init__(
        self,
        product_repository: ProdutoRepository,
        product_query: ProdutoQuery,
        category_query: CategoriaQuery,
        currency_query: CurrencyQuery,
    ):
        self.product_repository = product_repository
        self.product_query = product_query
        self.currency_query = currency_query
        self.category_query = category_query

    @abstractmethod
    def create_product(self, produto: PartialProdutoEntity) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def activate_product(self, product_id: int) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def deactivate_product(self, product_id: int) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def delete_product(self, product_id: int):
        raise NotImplementedError()

    @abstractmethod
    def update_product(self, produto: ProdutoEntity) -> ProdutoAggregate:
        raise NotImplementedError()
