from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    name: str
    allow_components: bool
    currency_id: int
    value: float
    category_id: int
