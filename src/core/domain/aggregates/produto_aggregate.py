from typing import List, Optional

from pydantic import Field
from src.core.domain.base.aggregate import AggregateRoot
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.produto_entity import ProdutoEntity


class ProdutoAggregate(AggregateRoot):
    product: ProdutoEntity
    orders: Optional[List[CompraEntity]] = None
    sold_amount: Optional[int] = Field(default=0)
