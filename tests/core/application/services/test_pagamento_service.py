from copy import deepcopy
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from src.core.application.services.pagamento_service import PagamentoService
from src.core.domain.aggregates.pagamento_aggregate import PagamentoAggregate
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.categoria_entity import CategoriaEntity
from src.core.domain.entities.cliente_entity import ClienteEntity
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.entities.currency_entity import CurrencyEntity
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.domain.entities.pagamento_entity import (
    PagamentoEntity,
    PartialPagamentoEntity,
)
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.domain.entities.produto_escolhido_entity import ProdutoEscolhidoEntity
from src.core.domain.value_objects.address_value_object import AddressValueObject
from src.core.domain.value_objects.persona_value_object import PersonaValueObject
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.enums.pagamento_status import PagamentoStatus


class TestPagamentoService:

    @pytest.fixture
    def meio_de_pagamento_query(self):
        return MagicMock()

    @pytest.fixture
    def purchase_query(self):
        return MagicMock()

    @pytest.fixture
    def pagamento_repository(self):
        return MagicMock()

    @pytest.fixture
    def pedido_repository(self):
        return MagicMock()

    @pytest.fixture
    def payment_provider(self):
        return MagicMock()

    @pytest.fixture
    def pagamento_service(
        self,
        pagamento_repository,
        purchase_query,
        payment_provider,
        meio_de_pagamento_query,
        pedido_repository,
    ):
        return PagamentoService(
            pagamento_repository=pagamento_repository,
            purchase_query=purchase_query,
            payment_provider=payment_provider,
            meio_de_pagamento_query=meio_de_pagamento_query,
            pedido_repository=pedido_repository,
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
            total=PrecoValueObject(value=10, currency=currency),
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )

    @pytest.fixture
    def payment_method_entity(self):
        return MeioDePagamentoEntity(
            id=1,
            name="mock_payment_method",
            sys_name="mock_payment_method",
            description="This is a mock payment method",
            is_active=True,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )

    @pytest.fixture
    def pagamento_entity(
        self,
        compra_entity: CompraEntity,
        preco: PrecoValueObject,
        payment_method_entity: MeioDePagamentoEntity,
    ):
        pagamento_price = deepcopy(preco)
        pagamento_price.value = 20
        return PagamentoEntity(
            id=1,
            payment_method=payment_method_entity,
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

    def test_process_payment_successfully(
        self,
        pagamento_service: PagamentoService,
        pedido_aggregate: PedidoAggregate,
        payment_method_entity: MeioDePagamentoEntity,
    ):
        pagamento_service.payment_provider.process_payment = MagicMock(
            return_value=True
        )
        pedido = deepcopy(pedido_aggregate)
        pedido.payment = None
        pagamento_service.purchase_query.get = MagicMock(return_value=pedido)
        pagamento_service.meio_de_pagamento_query.get = MagicMock(
            return_value=payment_method_entity
        )
        return_payment = PagamentoAggregate(
            payment=PartialPagamentoEntity(
                payment_method=payment_method_entity,
                status=PagamentoStatus.PAGO,
                purchase=pedido.purchase,
                payment_value=pedido.purchase.total,
            ),
            purchase=PartialCompraEntity(
                status=CompraStatus.PAGO,
            ),
        )
        pagamento_service.payment_repository.create = MagicMock(
            return_value=return_payment
        )
        pagamento_service.pedido_repository.update = MagicMock(
            return_value=return_payment
        )
        result = pagamento_service.process_purchase_payment(1, 1)
        assert result == return_payment

    def test_process_payment_fail_because_purchase_is_payed(
        self,
        pagamento_service: PagamentoService,
        pedido_aggregate: PedidoAggregate,
        payment_method_entity: MeioDePagamentoEntity,
    ):
        pagamento_service.payment_provider.process_payment = MagicMock(
            return_value=True
        )

        pagamento_service.purchase_query.get = MagicMock(return_value=pedido_aggregate)
        pagamento_service.meio_de_pagamento_query.get = MagicMock(
            return_value=payment_method_entity
        )
        with pytest.raises(ValueError, match="Pedido já foi pago."):
            pagamento_service.process_purchase_payment(1, 1)

    def test_process_payment_fail_because_purchase_doesnt_exists(
        self,
        pagamento_service: PagamentoService,
        pedido_aggregate: PedidoAggregate,
        payment_method_entity: MeioDePagamentoEntity,
    ):
        pagamento_service.payment_provider.process_payment = MagicMock(
            return_value=True
        )

        pagamento_service.purchase_query.get = MagicMock(return_value=None)
        pagamento_service.meio_de_pagamento_query.get = MagicMock(
            return_value=payment_method_entity
        )
        with pytest.raises(ValueError, match="Pedido não encontrado."):
            pagamento_service.process_purchase_payment(1, 1)

    def test_process_payment_fail_because_purchase_value_is_negative_or_zero(
        self,
        pagamento_service: PagamentoService,
        pedido_aggregate: PedidoAggregate,
        payment_method_entity: MeioDePagamentoEntity,
        currency: CurrencyEntity,
    ):
        pagamento_service.payment_provider.process_payment = MagicMock(
            return_value=True
        )
        pedido = deepcopy(pedido_aggregate)
        pedido.payment = None
        pedido.purchase.total = PrecoValueObject(value=0, currency=currency)
        pagamento_service.purchase_query.get = MagicMock(return_value=pedido)
        pagamento_service.meio_de_pagamento_query.get = MagicMock(
            return_value=payment_method_entity
        )
        with pytest.raises(
            ValueError, match="Valor do pedido não pode ser zero ou negativo"
        ):
            pagamento_service.process_purchase_payment(1, 1)
        pedido.purchase.total = PrecoValueObject(value=-10, currency=currency)
        pagamento_service.purchase_query.get = MagicMock(return_value=pedido)
        with pytest.raises(
            ValueError, match="Valor do pedido não pode ser zero ou negativo"
        ):
            pagamento_service.process_purchase_payment(1, 1)

    def test_process_payment_fail_because_purchase_isnt_criando_status(
        self,
        pagamento_service: PagamentoService,
        pedido_aggregate: PedidoAggregate,
        payment_method_entity: MeioDePagamentoEntity,
    ):
        pagamento_service.payment_provider.process_payment = MagicMock(
            return_value=True
        )
        pedido = deepcopy(pedido_aggregate)
        pedido.payment = None
        pedido.purchase.status = CompraStatus.CANCELADO
        pedido.purchase.total.value = 10
        pagamento_service.purchase_query.get = MagicMock(return_value=pedido)
        pagamento_service.meio_de_pagamento_query.get = MagicMock(
            return_value=payment_method_entity
        )
        with pytest.raises(ValueError, match="Pedido inválido para pagamento."):
            pagamento_service.process_purchase_payment(1, 1)

    def test_process_payment_fail_because_payment_method_doesnt_exists(
        self,
        pagamento_service: PagamentoService,
        pedido_aggregate: PedidoAggregate,
        payment_method_entity: MeioDePagamentoEntity,
    ):
        pagamento_service.payment_provider.process_payment = MagicMock(
            return_value=True
        )
        pedido = deepcopy(pedido_aggregate)
        pedido.payment = None
        pagamento_service.purchase_query.get = MagicMock(return_value=pedido)
        pagamento_service.meio_de_pagamento_query.get = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Meio de pagamento não encontrado."):
            pagamento_service.process_purchase_payment(1, 1)

    def test_process_payment_fail_because_payment_method_is_inactive(
        self,
        pagamento_service: PagamentoService,
        pedido_aggregate: PedidoAggregate,
        payment_method_entity: MeioDePagamentoEntity,
    ):
        pagamento_service.payment_provider.process_payment = MagicMock(
            return_value=True
        )
        payment_method = deepcopy(payment_method_entity)
        payment_method.is_active = False
        pedido = deepcopy(pedido_aggregate)
        pedido.payment = None
        pagamento_service.purchase_query.get = MagicMock(return_value=pedido)
        pagamento_service.meio_de_pagamento_query.get = MagicMock(
            return_value=payment_method
        )
        with pytest.raises(ValueError, match="Meio de pagamento inativo."):
            pagamento_service.process_purchase_payment(1, 1)
