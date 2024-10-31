from typing import Any

from src.adapters.data_mappers.cliente_aggregate_data_mapper import (
    ClienteAggregateDataMapper,
)
from src.adapters.data_mappers.cliente_entity_data_mapper import ClientEntityDataMapper
from src.adapters.driven.infra.models.persona import Persona
from src.adapters.driven.infra.ports.orm_cliente_query import OrmClienteQuery
from src.adapters.driven.infra.repositories.orm_repository import OrmRepository
from src.core.domain.aggregates.cliente_aggregate import ClienteAggregate
from src.core.domain.entities.cliente_entity import ClienteEntity, PartialClienteEntity
from src.core.domain.repositories.cliente_repository import ClienteRepository
from src.core.helpers.options.client_find_options import ClientFindOptions


class OrmClientRepository(OrmRepository, ClienteRepository):

    def create(self, produto: PartialClienteEntity) -> ClienteAggregate:
        db_item = ClientEntityDataMapper.from_domain_to_db(produto)
        client: Persona = Persona.create(**db_item)
        client.save()
        return ClienteAggregateDataMapper.from_db_to_domain(client)

    def update(self, produto: ClienteEntity) -> ClienteAggregate:
        raise NotImplementedError()

    def delete(self, produto_id: int):
        raise NotImplementedError()

    def get_by_purchase_id(self, produto_id: int) -> ClienteAggregate:
        raise NotImplementedError()

    def find(self, query_options: ClientFindOptions) -> list[ClienteAggregate]:
        return OrmClienteQuery().find(query_options)
