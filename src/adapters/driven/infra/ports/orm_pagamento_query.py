from src.core.application.ports.pagamento_query import PagamentoQuery
from src.core.domain.entities.pagamento_entity import (
    PagamentoEntity,
    PartialPagamentoEntity,
)


class OrmPagamentoQuery(PagamentoQuery):
    def get(self, item_id: int) -> PagamentoEntity:
        raise NotImplementedError()

    def get_all(self) -> list[PagamentoEntity]:
        raise NotImplementedError()

    def find(self, query_options: PartialPagamentoEntity) -> list[PagamentoEntity]:
        raise NotImplementedError()
