from typing import Optional

from src.core.domain.base.aggregate import AggregateRoot
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity


class PedidoAggregate(AggregateRoot):
    purchase: CompraEntity
    payment: Optional[PagamentoEntity] = None
