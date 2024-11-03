from typing import Optional
from pydantic import Field

from src.core.domain.base.entity import Entity, PartialEntity


class CurrencyEntity(Entity):
    symbol: str
    name: str
    code: str = Field(..., min_length=3, max_length=3)
    is_active: bool = Field(default=True)


class PartialCurrencyEntity(PartialEntity, CurrencyEntity):
    symbol: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = Field(default=None, min_length=3, max_length=3)
    is_active: Optional[bool] = Field(default=True)
