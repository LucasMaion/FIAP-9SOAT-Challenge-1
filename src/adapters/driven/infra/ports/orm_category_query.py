from src.core.application.ports.category_query import CategoryQuery
from src.core.domain.entities.categoria_entity import (
    CategoriaEntity,
    PartialCategoriaEntity,
)


class OrmCategoryQuery(CategoryQuery):
    def get(self, item_id: int) -> CategoriaEntity:
        return "YAY"

    def get_all(self) -> list[CategoriaEntity]:
        return "YAY"

    def find(self, query_options: PartialCategoriaEntity) -> list[CategoriaEntity]:
        return "YAY"
