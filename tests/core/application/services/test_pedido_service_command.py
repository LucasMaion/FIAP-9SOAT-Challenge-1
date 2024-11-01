from copy import deepcopy
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from src.core.application.ports.pedido_query import PedidoQuery
from src.core.application.ports.produto_query import ProdutoQuery
from src.core.application.services.pedido_service_command import PedidoServiceCommand
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.categoria_entity import CategoriaEntity
from src.core.domain.entities.cliente_entity import ClienteEntity
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.currency_entity import CurrencyEntity
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.domain.entities.produto_escolhido_entity import ProdutoEscolhidoEntity
from src.core.domain.value_objects.address_value_object import AddressValueObject
from src.core.domain.value_objects.persona_value_object import PersonaValueObject
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.enums.pagamento_status import PagamentoStatus
from src.core.helpers.interfaces.chace_service import CacheService


class TestPedidoService:
    @pytest.fixture
    def produto_query(self):
        return MagicMock()

    @pytest.fixture
    def purchase_query(self):
        return MagicMock()

    @pytest.fixture
    def purchase_repository(self):
        return MagicMock()

    @pytest.fixture
    def cache_service(self):
        return MagicMock()

    @pytest.fixture
    def purchase_service(
        self,
        purchase_repository: PedidoAggregate,
        purchase_query: PedidoQuery,
        produto_query: ProdutoQuery,
        cache_service: CacheService,
    ):
        cache_service.get = MagicMock(return_value=None)
        cache_service.set = MagicMock(return_value=None)
        return PedidoServiceCommand(
            purchase_repository=purchase_repository,
            purchase_query=purchase_query,
            produto_query=produto_query,
            cache_service=cache_service,
        )

    @pytest.fixture
    def currency(self):
        return CurrencyEntity(
            id=1,
            symbol="R$",
            name="Real",
            code="BRL",
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )

    @pytest.fixture
    def preco(self, currency: CurrencyEntity):
        return PrecoValueObject(
            value=10,
            currency=currency,
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

    @pytest.fixture
    def product_entity(self, preco: PrecoValueObject):
        produto_entity = ProdutoEntity(
            id=1,
            name="added_component",
            description="produto_test_mock",
            price=preco,
            category=CategoriaEntity(
                name="categoria",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            is_active=False,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
            allow_components=False,
        )
        components = [deepcopy(produto_entity) for _ in range(2)]
        for component in components:
            component.id += 1
        produto_entity.components = components
        return produto_entity

    @pytest.fixture
    def selected_product_entity(self, product_entity: ProdutoEntity):
        component = deepcopy(product_entity)
        component.id = 2
        return ProdutoEscolhidoEntity(
            id=1,
            product=product_entity,
            added_components=[component],
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )

    @pytest.fixture
    def compra_entity(
        self,
        client_entity: ClienteEntity,
        selected_product_entity: ProdutoEscolhidoEntity,
        currency: CurrencyEntity,
    ):
        return CompraEntity(
            id=1,
            client=client_entity,
            selected_products=[selected_product_entity],
            status=CompraStatus.CRIANDO,
            total=PrecoValueObject(value=0, currency=currency),
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )

    @pytest.fixture
    def pagamento_entity(self, compra_entity: CompraEntity, preco: PrecoValueObject):
        pagamento_price = deepcopy(preco)
        pagamento_price.value = 20
        return PagamentoEntity(
            id=1,
            payment_method=MeioDePagamentoEntity(
                id=1,
                name="mock_payment_method",
                sys_name="mock_payment_method",
                description="This is a mock payment method",
                is_active=True,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            payment_value=pagamento_price,
            status=PagamentoStatus.PAGO,
            purchase=compra_entity,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )

    @pytest.fixture
    def pedido_aggregate(
        self,
        compra_entity: CompraEntity,
        pagamento_entity: PagamentoEntity,
    ):
        return PedidoAggregate(
            purchase=compra_entity,
            payment=pagamento_entity,
        )

    def test_create_purchase_successfully(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=None
        )
        purchase_service.purchase_repository.create = MagicMock(
            return_value=pedido_aggregate.purchase
        )
        result = purchase_service.create_pedido(pedido=pedido_aggregate.purchase)
        assert result == pedido_aggregate.purchase
        purchase_service.purchase_repository.create.assert_called_once()

    def test_add_product_to_existing_purchase_successfully(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido_aggregate
        )
        purchase_service.produto_query.get_only_entity = MagicMock(
            return_value=pedido_aggregate.purchase.selected_products[0].product
        )
        purchase_service.purchase_repository.update = MagicMock(
            return_value=pedido_aggregate.purchase
        )
        result = purchase_service.add_new_product(1, 1)
        assert result == pedido_aggregate.purchase
        purchase_service.purchase_repository.update.assert_called_once()

    def test_add_product_to_existing_purchase_fail_because_purchase_doesnt_exists(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=None
        )
        purchase_service.produto_query.get_only_entity = MagicMock(
            return_value=pedido_aggregate.purchase.selected_products[0].product
        )
        with pytest.raises(ValueError, match="Pedido não encontrado"):
            purchase_service.add_new_product(1, 1)

    def test_add_product_to_existing_purchase_fail_because_product_doesnt_exists(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido_aggregate
        )
        purchase_service.produto_query.get_only_entity = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto não encontrado"):
            purchase_service.add_new_product(1, 1)

    def test_add_product_to_existing_purchase_fail_because_purchase_isnt_status_criando(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        pedido = deepcopy(pedido_aggregate)
        pedido.purchase.status = CompraStatus.CONCLUIDO
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido
        )
        purchase_service.produto_query.get_only_entity = MagicMock(return_value=pedido)
        with pytest.raises(ValueError, match="Pedido não está mais aberto."):
            purchase_service.add_new_product(1, 1)

    def test_add_component_to_product_in_purchase_successfully(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido_aggregate
        )
        purchase_service.produto_query.get_only_entity = MagicMock(
            side_effect=[
                pedido_aggregate.purchase.selected_products[0].product,
                pedido_aggregate.purchase.selected_products[0].product.components[0],
            ]
        )
        purchase_service.purchase_repository.update = MagicMock(
            return_value=pedido_aggregate.purchase
        )
        result = purchase_service.add_component_to_select_product(1, 1, 2)
        assert result == pedido_aggregate.purchase
        purchase_service.purchase_repository.update.assert_called_once()

    def test_add_component_to_product_in_purchase_fail_because_component_isnt_associated_to_product(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        component = deepcopy(pedido_aggregate.purchase.selected_products[0].product)
        component.id = 3
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido_aggregate
        )
        purchase_service.produto_query.get_only_entity = MagicMock(
            side_effect=[
                pedido_aggregate.purchase.selected_products[0].product,
                component,
            ]
        )
        with pytest.raises(ValueError, match="Produto não possui esse adicional."):
            purchase_service.add_component_to_select_product(1, 1, 3)

    def test_remove_product_from_purchase_successfully(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido_aggregate
        )

        purchase_service.purchase_repository.update = MagicMock(
            return_value=pedido_aggregate.purchase
        )
        result = purchase_service.remove_select_product(1, 1)
        assert result == pedido_aggregate.purchase
        purchase_service.purchase_repository.update.assert_called_once()

    def test_remove_product_from_purchase_fail_because_product_isnt_associated_to_purchase(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido_aggregate
        )
        with pytest.raises(ValueError, match="Produto não está no pedido."):
            purchase_service.remove_select_product(1, 3)

    def test_concludes_a_purchase_successfully(
        self,
        purchase_service: PedidoServiceCommand,
        pedido_aggregate: PedidoAggregate,
        currency: CurrencyEntity,
    ):
        pedido = deepcopy(pedido_aggregate)
        pedido.purchase.total = PrecoValueObject(value=10, currency=currency)
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido
        )
        purchase_service.purchase_repository.update = MagicMock(
            return_value=pedido.purchase
        )
        result = purchase_service.concludes_pedido(1)
        assert result == pedido.purchase
        purchase_service.purchase_repository.update.assert_called_once()

    def test_concludes_a_purchase_fail_because_purchase_doesnt_existis(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=None
        )
        with pytest.raises(ValueError, match="Pedido não encontrado."):
            purchase_service.concludes_pedido(1)

    def test_concludes_a_purchase_fail_because_value_is_invalid_zero_or_negative(
        self,
        purchase_service: PedidoServiceCommand,
        pedido_aggregate: PedidoAggregate,
        currency: CurrencyEntity,
    ):
        purchase = deepcopy(pedido_aggregate)
        purchase.purchase.total = PrecoValueObject(value=0, currency=currency)
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(ValueError, match="Valor do pedido é zero."):
            purchase_service.concludes_pedido(1)
        purchase.purchase.total = PrecoValueObject(value=-10, currency=currency)
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(ValueError, match="Valor do pedido é negativo."):
            purchase_service.concludes_pedido(1)

    def test_concludes_a_purchase_fail_because_there_are_no_products_associated(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase = deepcopy(pedido_aggregate)
        purchase.purchase.selected_products = []
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(ValueError, match="Pedido não possui produtos."):
            purchase_service.concludes_pedido(1)

    def test_concludes_a_purchase_fail_because_there_is_no_successful_payment_associated(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase = deepcopy(pedido_aggregate)
        purchase.payment = None
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(ValueError, match="Pedido não possui pagamento efetuado."):
            purchase_service.concludes_pedido(1)

    def test_concludes_a_purchase_fail_because_purchase_is_already_concluded(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase = deepcopy(pedido_aggregate)
        purchase.payment.status = PagamentoStatus.PENDENTE
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(ValueError, match="Pedido não possui pagamento efetuado."):
            purchase_service.concludes_pedido(1)
        purchase.payment.status = PagamentoStatus.CANCELADO
        with pytest.raises(ValueError, match="Pedido não possui pagamento efetuado."):
            purchase_service.concludes_pedido(1)

    def test_cancels_purchase_successfully(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        pedido = deepcopy(pedido_aggregate)
        pedido.purchase.status = CompraStatus.CRIANDO
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=pedido
        )
        purchase_service.cancel_pedido(1)

    def test_cancels_purchase_fail_because_purchase_doesnt_existis(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=None
        )
        with pytest.raises(ValueError, match="Pedido não encontrado."):
            purchase_service.cancel_pedido(1)

    def test_cancels_purchase_fail_because_purchase_is_already_finalized(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase = deepcopy(pedido_aggregate)
        purchase.purchase.status = CompraStatus.FINALIZADO
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(
            ValueError,
            match=f"Não é permitido mudar do status {CompraStatus.FINALIZADO.name} para o status {CompraStatus.CANCELADO.name}",
        ):
            purchase_service.cancel_pedido(1)

    def test_cancels_purchase_fail_because_purchase_is_already_canceled(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        purchase = deepcopy(pedido_aggregate)
        purchase.purchase.status = CompraStatus.CANCELADO
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(
            ValueError,
            match=f"Não é permitido mudar do status {CompraStatus.CANCELADO.name} para o status {CompraStatus.CANCELADO.name}",
        ):
            purchase_service.cancel_pedido(1)

    def test_update_status_successfully(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        new_status = CompraStatus.ENTREGUE
        purchase = deepcopy(pedido_aggregate)
        purchase.purchase.status = CompraStatus.EM_PREPARO
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        purchase_service.update_status(1, new_status)

    def test_update_status_fail_because_new_status_break_state_machine_rules(
        self, purchase_service: PedidoServiceCommand, pedido_aggregate: PedidoAggregate
    ):
        new_status = CompraStatus.CRIANDO
        purchase = deepcopy(pedido_aggregate)
        purchase.purchase.status = CompraStatus.CONCLUIDO
        purchase_service.purchase_repository.get_by_purchase_id = MagicMock(
            return_value=purchase
        )
        with pytest.raises(
            ValueError,
            match=f"Não é permitido mudar do status {purchase.purchase.status.name} para o status {new_status.name}",
        ):
            purchase_service.update_status(1, new_status)
