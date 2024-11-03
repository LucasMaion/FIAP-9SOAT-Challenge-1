from typing import Optional
from src.core.domain.base.entity import Entity, PartialEntity
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.pagamento_status import PagamentoStatus


class PagamentoEntity(Entity):
    payment_method: MeioDePagamentoEntity
    payment_value: PrecoValueObject
    status: PagamentoStatus


class PartialPagamentoEntity(PartialEntity, PagamentoEntity):
    payment_method: Optional[MeioDePagamentoEntity] = None
    payment_value: Optional[PrecoValueObject] = None
    status: Optional[PagamentoStatus] = None
