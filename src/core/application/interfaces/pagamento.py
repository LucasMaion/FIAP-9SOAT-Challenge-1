from abc import ABC, abstractmethod
from typing import List

from src.adapters.driven.payment_providers.interfaces.payment_provider import (
    PaymentProvider,
)
from src.core.application.ports.meio_de_pagamento_query import MeioDePagamentoQuery
from src.core.application.ports.pedido_query import PedidoQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.repositories.pedido_repository import PedidoRepository


class IPagamentoService(ABC):
    def __init__(
        self,
        purchase_repository: PedidoRepository,
        purchase_query: PedidoQuery,
        meio_de_pagamento_query: MeioDePagamentoQuery,
        payment_provider: PaymentProvider,
    ):
        self.purchase_repository = purchase_repository
        self.purchase_query = purchase_query
        self.payment_provider = payment_provider
        self.meio_de_pagamento_query = meio_de_pagamento_query

    @abstractmethod
    def process_purchase_payment(
        self, pedido_id: int, payment_method_id: int
    ) -> PedidoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def list_payment_methods(self) -> List[MeioDePagamentoQuery]:
        raise NotImplementedError()
