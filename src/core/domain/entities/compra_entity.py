from decimal import Decimal
from typing import List, Optional
from src.core.domain.base.entity import Entity, PartialEntity


class CompraEntity(Entity):
    client_id: int
    status: str
    products_id: List[int]
    total: Decimal
    finalized: bool
    canceled: bool


class PartialCompraEntity(PartialEntity, CompraEntity):
    client_id: Optional[int] = None
    status: Optional[str] = None
    products_id: Optional[List[int]] = None
    total: Optional[Decimal] = None
