from abc import ABC, abstractmethod

from src.core.domain.entities.pagamento_entity import (
    PagamentoEntity,
    PartialPagamentoEntity,
)


class PagamentoQuery(ABC):
    @abstractmethod
    def get(self, item_id: int) -> PagamentoEntity:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[PagamentoEntity]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: PartialPagamentoEntity) -> list[PagamentoEntity]:
        raise NotImplementedError()
