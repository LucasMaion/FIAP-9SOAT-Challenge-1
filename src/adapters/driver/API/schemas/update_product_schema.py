from pydantic import BaseModel


class UpdateProductSchema(BaseModel):
    id: int
    name: str
    allow_components: bool
    currency_id: int
    value: float
    category_id: int
    component_ids: list[int]
