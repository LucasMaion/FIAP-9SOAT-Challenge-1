from typing import Optional
from pydantic import BaseModel
from src.core.domain.base.aggregate import AggregateRoot
from src.core.domain.entities.cliente_entity import ClienteEntity
from src.core.domain.entities.compra_entity import CompraEntity


class ClienteAggregate(AggregateRoot, BaseModel):
    client: ClienteEntity
    orders: Optional[list[CompraEntity]] = None
