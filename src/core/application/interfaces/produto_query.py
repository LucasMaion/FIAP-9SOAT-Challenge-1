from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.application.ports.produto_query import ProdutoQuery
from src.core.application.ports.categoria_query import CategoriaQuery
from src.core.application.ports.currency_query import CurrencyQuery
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.categoria_entity import CategoriaEntity
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class IProdutoQuery(ABC):
    def __init__(
        self,
        product_query: ProdutoQuery,
        category_query: CategoriaQuery,
        currency_query: CurrencyQuery,
    ):
        self.product_query = product_query
        self.currency_query = currency_query
        self.category_query = category_query

    @abstractmethod
    def get(self, product_id: int) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def index(
        self, options: Optional[ProdutoFindOptions] = None
    ) -> List[ProdutoAggregate]:
        raise NotImplementedError()

    @abstractmethod
    def list_categories(self) -> List[CategoriaEntity]:
        raise NotImplementedError()
