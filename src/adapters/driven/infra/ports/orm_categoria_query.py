from src.adapters.data_mappers.categoria_entity_data_mapper import (
    CategoriaEntityDataMapper,
)
from src.adapters.driven.infra.models.categories import Category
from src.core.application.ports.categoria_query import CategoriaQuery
from src.core.domain.entities.categoria_entity import (
    CategoriaEntity,
    PartialCategoriaEntity,
)


class OrmCategoriaQuery(CategoriaQuery):
    def get(self, item_id: int) -> CategoriaEntity:
        product: Category = Category.select().where(Category.id == item_id)
        parsed_result = [
            CategoriaEntityDataMapper.from_db_to_domain(res) for res in product
        ]
        if len(parsed_result) == 1:
            return parsed_result[0]
        return None

    def get_all(self) -> list[CategoriaEntity]:
        product: Category = Category.select()
        parsed_result = [
            CategoriaEntityDataMapper.from_db_to_domain(res) for res in product
        ]
        return parsed_result

    def find(self, query_options: PartialCategoriaEntity) -> list[CategoriaEntity]:
        raise NotImplementedError()
