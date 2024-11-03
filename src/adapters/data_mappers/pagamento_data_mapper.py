from decimal import Decimal
from typing import Optional
from src.adapters.data_mappers.currency_entity_data_mapper import (
    CurrencyEntityDataMapper,
)
from src.adapters.data_mappers.meio_de_pagamento_data_mapper import (
    MeioDePagamentoEntityDataMapper,
)
from src.adapters.driven.infra.models.payments import Payment
from src.core.domain.entities.compra_entity import PartialCompraEntity
from src.core.domain.entities.pagamento_entity import (
    PartialPagamentoEntity,
)
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.pagamento_status import PagamentoStatus


class PagamentoEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, payment: Payment):
        return PartialPagamentoEntity(
            id=payment.id,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            deleted_at=payment.deleted_at,
            payment_method=MeioDePagamentoEntityDataMapper.from_db_to_domain(
                payment.payment_method
            ),
            status=PagamentoStatus(payment.status),
            payment_value=PrecoValueObject(
                value=Decimal(payment.value),
                currency=CurrencyEntityDataMapper.from_db_to_domain(payment.currency),
            ),
        )

    @classmethod
    def from_domain_to_db(
        cls,
        payment: PartialPagamentoEntity,
        purchase: Optional[PartialCompraEntity] = None,
    ):
        return {
            "id": payment.id,
            "payment_method": payment.payment_method.id,
            "status": payment.status.value,
            "value": payment.payment_value.value,
            "currency": payment.payment_value.currency.id,
            "purchase": purchase.id if purchase else None,
        }
