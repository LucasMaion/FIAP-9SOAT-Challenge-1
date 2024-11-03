from typing import List, Optional
from pydantic import Field

from src.core.domain.base.entity import Entity, PartialEntity
from src.core.domain.entities.categoria_entity import CategoriaEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject


class ProdutoEntity(Entity):
    name: str = Field(..., min_length=1)
    category: Optional[CategoriaEntity] = None
    price: Optional[PrecoValueObject] = None
    components: Optional[List["ProdutoEntity"]] = None
    is_active: bool = Field(default=False)
    allow_components: bool = Field(default=False)


class PartialProdutoEntity(PartialEntity, ProdutoEntity):
    name: str = Field(default=None, min_length=1)
