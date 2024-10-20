from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: int = Field(..., gt=0)
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False


class PartialEntity(BaseModel):
    id: Optional[int] = Field(default=None, gt=0)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
