from typing import Optional
from src.core.domain.base.entity import Entity
from src.core.domain.value_objects.persona_value_object import PersonaValueObject


class UsuarioEntity(Entity):
    username: str
    password: str
    person: Optional[PersonaValueObject] = None
