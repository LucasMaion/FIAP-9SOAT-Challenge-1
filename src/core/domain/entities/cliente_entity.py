from typing import Optional
from src.core.domain.base.entity import Entity, PartialEntity
from src.core.domain.value_objects.persona_value_object import PersonaValueObject


class ClienteEntity(Entity):
    user_id: Optional[int] = None
    person: PersonaValueObject


class PartialClienteEntity(PartialEntity, ClienteEntity):
    user_id: Optional[int] = None
    person: Optional[PersonaValueObject] = None
