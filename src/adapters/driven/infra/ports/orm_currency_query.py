from src.core.application.ports.currency_query import CurrencyQuery
from src.core.domain.entities.currency_entity import (
    CurrencyEntity,
    PartialCurrencyEntity,
)


class OrmCurrencyQuery(CurrencyQuery):
    def get(self, item_id: int) -> CurrencyEntity:
        return "YAY"

    def get_all(self) -> list[CurrencyEntity]:
        return "YAY"

    def find(self, query_options: PartialCurrencyEntity) -> list[CurrencyEntity]:
        return "YAY"
