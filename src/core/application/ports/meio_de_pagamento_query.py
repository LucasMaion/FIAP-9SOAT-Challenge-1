from abc import ABC, abstractmethod
from typing import Union

from src.core.domain.entities.meio_de_pagamento_entity import (
    MeioDePagamentoEntity,
    PartialMeioDePagamentoEntity,
)


class MeioDePagamentoQuery(ABC):
    @abstractmethod
    def get(self, item_id: int) -> Union[MeioDePagamentoEntity, None]:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[MeioDePagamentoEntity]:
        raise NotImplementedError()

    @abstractmethod
    def find(
        self, query_options: PartialMeioDePagamentoEntity
    ) -> list[MeioDePagamentoEntity]:
        raise NotImplementedError()
