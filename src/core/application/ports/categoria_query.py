from abc import ABC, abstractmethod

from src.core.domain.entities.categoria_entity import (
    CategoriaEntity,
    PartialCategoriaEntity,
)


class CategoriaQuery(ABC):
    @abstractmethod
    def get(self, item_id: int) -> CategoriaEntity:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[CategoriaEntity]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: PartialCategoriaEntity) -> list[CategoriaEntity]:
        raise NotImplementedError()
