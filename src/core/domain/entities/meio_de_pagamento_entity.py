from typing import Optional
from src.core.domain.base.entity import Entity, PartialEntity


class MeioDePagamentoEntity(Entity):
    name: str
    sys_name: str
    description: str
    is_active: bool


class PartialMeioDePagamentoEntity(PartialEntity, MeioDePagamentoEntity):
    name: Optional[str] = None
    sys_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
