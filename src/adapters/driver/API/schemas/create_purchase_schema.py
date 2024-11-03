from typing import Optional
from pydantic import BaseModel


class CreatePurchaseSchema(BaseModel):
    client_id: Optional[int] = None
    currency_id: int
