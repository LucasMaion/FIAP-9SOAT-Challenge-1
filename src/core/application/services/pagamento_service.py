from src.core.application.interfaces.pagamento import IPagamentoService
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.pagamento_entity import PartialPagamentoEntity
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.enums.pagamento_status import PagamentoStatus


class PagamentoService(IPagamentoService):
    def process_purchase_payment(
        self, pedido_id: int, payment_method_id: int
    ) -> PedidoAggregate:
        pedido = self.purchase_query.get(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado.")
        if pedido.payment:
            raise ValueError("Pedido já foi pago.")
        if pedido.purchase.total.value <= 0:
            raise ValueError("Valor do pedido não pode ser zero ou negativo")
        if pedido.purchase.status != CompraStatus.CRIANDO:
            raise ValueError("Pedido inválido para pagamento.")
        payment_method = self.meio_de_pagamento_query.get(payment_method_id)
        if not payment_method:
            raise ValueError("Meio de pagamento não encontrado.")
        if payment_method.is_active is False:
            raise ValueError("Meio de pagamento inativo.")
        if self.payment_provider.process_payment(pedido, payment_method):
            payment = PartialPagamentoEntity(
                payment_method=payment_method,
                status=PagamentoStatus.PAGO,
                purchase=pedido.purchase,
                payment_value=pedido.purchase.total,
            )
            return self.purchase_repository.create_payment(payment)
        raise ValueError("Payment failed")