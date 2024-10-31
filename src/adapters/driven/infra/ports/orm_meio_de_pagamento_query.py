from src.core.application.ports.meio_de_pagamento_query import MeioDePagamentoQuery
from src.core.domain.entities.meio_de_pagamento_entity import (
    MeioDePagamentoEntity,
    PartialMeioDePagamentoEntity,
)


class OrmMeioDePagamentoQuery(MeioDePagamentoQuery):
    def get(self, item_id: int) -> MeioDePagamentoEntity:
        # TODO
        raise NotImplementedError()

    def get_all(self) -> list[MeioDePagamentoEntity]:
        # TODO
        raise NotImplementedError()

    def find(
        self, query_options: PartialMeioDePagamentoEntity
    ) -> list[MeioDePagamentoEntity]:
        raise NotImplementedError()
