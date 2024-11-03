from src.adapters.driven.infra.models.payment_methods import PaymentMethod
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity


class MeioDePagamentoEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, payment_method: PaymentMethod):
        return MeioDePagamentoEntity(
            id=payment_method.id,
            sys_name=payment_method.sys_name,
            created_at=payment_method.created_at,
            updated_at=payment_method.updated_at,
            deleted_at=payment_method.deleted_at,
            name=payment_method.name,
            description=payment_method.description,
            is_active=payment_method.is_active,
        )
