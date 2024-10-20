from abc import ABC, abstractmethod

from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity


class CompraQuery(ABC):
    @abstractmethod
    def get(self, item_id: int) -> CompraEntity:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[CompraEntity]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: PartialCompraEntity) -> list[CompraEntity]:
        raise NotImplementedError()
