from src.core.domain.base.aggregate import AggregateRoot
from src.core.domain.entities.cliente_entity import ClientEntity


class ClientAggregate(AggregateRoot):
    user: ClientEntity
