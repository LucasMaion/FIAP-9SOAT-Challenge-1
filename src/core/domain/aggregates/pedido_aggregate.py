from typing import List, Optional

from src.core.domain.base.aggregate import AggregateRoot
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity
from src.core.domain.entities.produto_entity import ProdutoEntity


class PedidoAggregate(AggregateRoot):
    purchase: CompraEntity
    products: Optional[List[ProdutoEntity]] = None
    payment: Optional[PagamentoEntity] = None
