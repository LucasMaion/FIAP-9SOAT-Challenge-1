from src.core.application.ports.currency_query import CurrencyQuery
from src.core.domain.entities.currency_entity import (
    CurrencyEntity,
    PartialCurrencyEntity,
)


class OrmCurrencyQuery(CurrencyQuery):
    def get(self, item_id: int) -> CurrencyEntity:
        #
        raise NotImplementedError()

    def get_all(self) -> list[CurrencyEntity]:
        raise NotImplementedError()

    def find(self, query_options: PartialCurrencyEntity) -> list[CurrencyEntity]:
        raise NotImplementedError()
