from abc import ABC, abstractmethod

from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity


class PaymentProvider(ABC):
    @abstractmethod
    def process_payment(self, compra: CompraEntity) -> PagamentoEntity:
        raise NotImplementedError()
