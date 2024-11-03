from fastapi import APIRouter, HTTPException
from loguru import logger
from src.adapters.driven.infra.ports.orm_meio_de_pagamento_query import (
    OrmMeioDePagamentoQuery,
)
from src.adapters.driven.infra.ports.orm_pedido_query import OrmPedidoQuery
from src.adapters.driven.infra.repositories.orm_pagamento_repository import (
    OrmPagamentoRepository,
)
from src.adapters.driven.infra.repositories.orm_pedido_repository import (
    OrmPedidoRepository,
)
from src.adapters.driven.payment_providers.functions.get_payment_provider_from_sys_name import (
    get_payment_provider_from_sys_name,
)
from src.adapters.driven.payment_providers.providers.default_provider import (
    DefaultPaymentProvider,
)
from src.core.application.services.pagamento_service import PagamentoService
from src.core.domain.aggregates.pagamento_aggregate import PagamentoAggregate
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.helpers.services.in_memory_cache import InMemoryCacheService

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
)


@router.post("/{pedido_id}/{payment_method_id}")
async def make_payment(pedido_id: int, payment_method_id: int) -> PagamentoAggregate:
    try:
        pedido_command = PagamentoService(
            OrmPagamentoRepository(),
            OrmPedidoRepository(InMemoryCacheService()),
            OrmPedidoQuery(),
            OrmMeioDePagamentoQuery(),
            DefaultPaymentProvider(),
        )
        payment_method = pedido_command.get_payment_method(payment_method_id)
        correct_payment_provider = get_payment_provider_from_sys_name(
            payment_method.sys_name
        )
        pedido_command.payment_provider = correct_payment_provider()
        return pedido_command.process_purchase_payment(pedido_id, payment_method_id)
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/methods")
async def list_payment_methods() -> list[MeioDePagamentoEntity]:
    try:
        pedido_command = PagamentoService(
            OrmPagamentoRepository(),
            OrmPedidoRepository(InMemoryCacheService()),
            OrmPedidoQuery(),
            OrmMeioDePagamentoQuery(),
            DefaultPaymentProvider(),
        )
        return pedido_command.list_payment_methods()
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
