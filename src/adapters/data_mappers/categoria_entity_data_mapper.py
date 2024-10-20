from src.adapters.driven.infra.models.categories import Category
from src.core.domain.entities.categoria_entity import PartialCategoriaEntity


class CategoriaEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, category: Category):
        return PartialCategoriaEntity(
            id=category.id,
            description=category.description,
            is_component=category.is_component,
            created_at=category.created_at,
            updated_at=category.updated_at,
            deleted_at=category.deleted_at,
        )
