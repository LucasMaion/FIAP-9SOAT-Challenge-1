from abc import ABC, abstractmethod

from src.core.domain.aggregates.pagamento_aggregate import PagamentoAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.pagamento_entity import PartialPagamentoEntity


class PagamentoRepository(Repository, ABC):

    @abstractmethod
    def create(self, payment: PartialPagamentoEntity) -> PagamentoAggregate:
        raise NotImplementedError()
