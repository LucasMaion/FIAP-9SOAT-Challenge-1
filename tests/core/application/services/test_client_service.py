from copy import deepcopy
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from src.core.application.services.cliente_service import ClienteCommand
from src.core.domain.entities.cliente_entity import ClienteEntity
from src.core.domain.value_objects.address_value_object import AddressValueObject
from src.core.domain.value_objects.persona_value_object import PersonaValueObject


class TestClientService:
    @pytest.fixture
    def cliente_query(self):
        return MagicMock()

    @pytest.fixture
    def cliente_repository(self):
        return MagicMock()

    @pytest.fixture
    def client_service(
        self,
        cliente_repository,
        cliente_query,
    ):
        return ClienteCommand(
            cliente_repository=cliente_repository,
            cliente_query=cliente_query,
        )

    @pytest.fixture
    def client_entity(self):
        return ClienteEntity(
            id=1,
            orders=[],
            person=PersonaValueObject(
                name="Test",
                document="12345678900",
                email="email.test@teste.test",
                address=AddressValueObject(
                    zip_code="12345678",
                    street="Test",
                    number="123",
                    city="Test",
                    state="Test",
                    country="Test",
                    additional_information="Test",
                ),
                birth_date=datetime(2021, 1, 1),
                phone="11999999999",
            ),
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )

    def test_create_client_should_create_new_client_with_document_name_and_email(
        self, client_service: ClienteCommand, client_entity: ClienteEntity
    ):
        expected_result = deepcopy(client_entity)
        del client_entity.id
        client_service.client_query.find = MagicMock(return_value=None)
        client_service.client_repository.create = MagicMock(
            return_value=expected_result
        )
        client = client_service.create_client(client_entity)
        assert client == expected_result
        client_service.client_repository.create.assert_called_once()

    def test_create_client_should_not_create_client_with_duplicated_document(
        self, client_service: ClienteCommand, client_entity: ClienteEntity
    ):
        expected_result = deepcopy(client_entity)
        del client_entity.id
        client_service.client_query.find = MagicMock(return_value=expected_result)
        client_service.client_repository.create = MagicMock(
            return_value=expected_result
        )
        with pytest.raises(ValueError, match="Cliente já cadastrado"):
            client_service.create_client(client_entity)
        client_service.client_repository.create.assert_not_called()

    def test_create_client_should_not_create_client_with_duplicated_email(
        self, client_service: ClienteCommand, client_entity: ClienteEntity
    ):
        expected_result = deepcopy(client_entity)
        del client_entity.id
        client_service.client_query.find = MagicMock(return_value=expected_result)
        client_service.client_repository.create = MagicMock(
            return_value=expected_result
        )
        with pytest.raises(ValueError, match="Cliente já cadastrado"):
            client_service.create_client(client_entity)
        client_service.client_repository.create.assert_not_called()
