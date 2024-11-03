from src.core.application.interfaces.cliente import IClienteService
from src.core.application.ports.cliente_query import ClienteQuery
from src.core.domain.aggregates.cliente_aggregate import ClienteAggregate
from src.core.domain.entities.cliente_entity import PartialClienteEntity
from src.core.domain.repositories.cliente_repository import ClienteRepository
from src.core.helpers.options.client_find_options import ClientFindOptions


class ClienteCommand(IClienteService):
    def __init__(
        self, cliente_repository: ClienteRepository, cliente_query: ClienteQuery
    ):
        self.client_repository = cliente_repository
        self.client_query = cliente_query

    def create_client(self, client: PartialClienteEntity) -> ClienteAggregate:
        existing_client = self.client_query.find(
            ClientFindOptions(
                document=client.person.document, email=client.person.email
            )
        )
        if existing_client:
            raise ValueError("Cliente já cadastrado")
        return self.client_repository.create(client)

    def get_client_by_document(self, document: str) -> ClienteAggregate:
        result = self.client_query.find(ClientFindOptions(document=document))
        if len(result) == 1:
            return result[0]
        return None

    def get_client_by_email(self, email: str) -> ClienteAggregate:
        result = self.client_query.find(ClientFindOptions(email=email))
        if len(result) == 1:
            return result[0]
        return None
