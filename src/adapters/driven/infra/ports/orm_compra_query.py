from src.core.application.ports.compra_query import CompraQuery
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity


class OrmCompraQuery(CompraQuery):
    def get(self, item_id: int) -> CompraEntity:
        return "YAY"

    def get_all(self) -> list[CompraEntity]:
        return "YAY"

    def find(self, query_options: PartialCompraEntity) -> list[CompraEntity]:
        return "YAY"
