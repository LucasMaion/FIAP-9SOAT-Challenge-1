from peewee import JOIN

from src.adapters.data_mappers.cliente_aggregate_data_mapper import (
    ClienteAggregateDataMapper,
)
from src.adapters.driven.infra.models.address import Address
from src.adapters.driven.infra.models.persona import Persona
from src.adapters.driven.infra.models.purchases import Purchase
from src.core.application.ports.cliente_query import ClienteQuery
from src.core.domain.aggregates.cliente_aggregate import ClienteAggregate
from src.core.helpers.options.client_find_options import ClientFindOptions


class OrmClienteQuery(ClienteQuery):
    def get(self, item_id: int) -> ClienteAggregate:
        raise NotImplementedError()

    def get_all(self) -> list[ClienteAggregate]:
        raise NotImplementedError()

    def find(self, query_options: ClientFindOptions) -> list[ClienteAggregate]:
        queries = []
        if query_options.name:
            queries.append(Persona.name.contains(query_options.name))
        if query_options.document:
            queries.append(Persona.document.contains(query_options.document))
        if query_options.email:
            queries.append(Persona.email.contains(query_options.email))

        result = (
            Persona.select()
            .join(
                Address,
                on=(Persona.address == Address.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Persona)
            .join(
                Purchase,
                on=(Purchase.client == Persona.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .where(*queries)
        )
        parsed_result = [
            ClienteAggregateDataMapper.from_db_to_domain(res, res.purchases)
            for res in result
        ]
        return parsed_result
