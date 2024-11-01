from typing import List, Optional
from src.core.application.interfaces.produto_query import IProdutoQuery
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.categoria_entity import CategoriaEntity
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class ProdutoServiceQuery(IProdutoQuery):

    def get(self, product_id: int) -> ProdutoAggregate:
        product = self.product_query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")
        return product

    def index(
        self, options: Optional[ProdutoFindOptions] = None
    ) -> List[ProdutoAggregate]:
        if not options:
            return self.product_query.get_all()
        return self.product_query.find(options)

    def list_categories(self) -> List[CategoriaEntity]:
        return self.category_query.get_all()
