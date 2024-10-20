from typing import List, Optional
from src.core.application.interfaces.product_query import IProductQuery
from src.core.application.ports.category_query import CategoryQuery
from src.core.application.ports.currency_query import CurrencyQuery
from src.core.application.ports.product_query import ProductQuery
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class ProductServiceQuery(IProductQuery):

    def get(self, product_id: int) -> ProdutoAggregate:
        product = self.product_query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")

    def index(
        self, options: Optional[ProdutoFindOptions] = None
    ) -> List[ProdutoAggregate]:
        if not options:
            return self.product_query.get_all()
        return self.product_query.find(options)
