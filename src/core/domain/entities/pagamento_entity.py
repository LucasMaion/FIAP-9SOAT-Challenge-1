from typing import Optional
from src.core.domain.base.entity import Entity, PartialEntity
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject


class PagamentoEntity(Entity):
    payment_method: MeioDePagamentoEntity
    payment_value: PrecoValueObject
    purchase_id: int


class PartialPagamentoEntity(PartialEntity, PagamentoEntity):
    payment_method: Optional[MeioDePagamentoEntity] = None
    payment_value: Optional[PrecoValueObject] = None
    purchase_id: Optional[int] = None
