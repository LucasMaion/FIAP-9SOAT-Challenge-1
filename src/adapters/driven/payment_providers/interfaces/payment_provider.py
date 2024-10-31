from abc import ABC, abstractmethod

from src.core.domain.entities.pagamento_entity import PagamentoEntity


class PaymentProvider(ABC):
    @abstractmethod
    def process_payment(self, payment: PagamentoEntity) -> dict:
        raise NotImplementedError()
