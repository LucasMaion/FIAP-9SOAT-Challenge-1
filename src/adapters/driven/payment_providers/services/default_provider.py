from src.adapters.driven.payment_providers.interfaces.payment_provider import (
    PaymentProvider,
)
from src.core.domain.entities.pagamento_entity import PagamentoEntity


class DefaultProvider(PaymentProvider):

    def process_payment(self, payment: PagamentoEntity) -> bool:
        return True
