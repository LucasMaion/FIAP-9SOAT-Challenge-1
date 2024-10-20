from typing import Optional
from pydantic import Field

from src.core.domain.base.entity import Entity, PartialEntity


# TODO: Add a category mapped with Literal or enum (lanche, acompanhamento, bebida, sobremesa, etc)
class CategoriaEntity(Entity):
    name: str
    description: Optional[str] = None
    is_component: bool = Field(default=False)


class PartialCategoriaEntity(PartialEntity, CategoriaEntity):
    name: Optional[str] = None