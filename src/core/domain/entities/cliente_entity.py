from typing import Optional
from src.core.domain.base.entity import Entity, PartialEntity


class ClientEntity(Entity):
    user_id: int


class PartialClientEntity(PartialEntity, ClientEntity):
    user_id: Optional[int] = None
