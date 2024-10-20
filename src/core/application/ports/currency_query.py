from abc import ABC, abstractmethod

from src.core.domain.entities.currency_entity import (
    CurrencyEntity,
    PartialCurrencyEntity,
)


class CurrencyQuery(ABC):
    @abstractmethod
    def get(self, item_id: int) -> CurrencyEntity:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[CurrencyEntity]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: PartialCurrencyEntity) -> list[CurrencyEntity]:
        raise NotImplementedError()
