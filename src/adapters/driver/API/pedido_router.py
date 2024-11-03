from typing import Annotated, List, Optional, Union
from loguru import logger
from fastapi import APIRouter, HTTPException, Query

from src.adapters.driven.infra.ports.orm_pedido_query import OrmPedidoQuery
from src.adapters.driven.infra.ports.orm_produto_query import OrmProductQuery
from src.adapters.driven.infra.repositories.orm_pedido_repository import (
    OrmPedidoRepository,
)
from src.adapters.driver.API.schemas.create_purchase_schema import CreatePurchaseSchema
from src.core.application.services.pedido_service_command import PedidoServiceCommand
from src.core.application.services.pedido_service_query import PedidoServiceQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.cliente_entity import PartialClienteEntity
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.entities.currency_entity import PartialCurrencyEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.functions.structure_value_range import structure_value_range
from src.core.helpers.options.pedido_find_options import PedidoFindOptions
from src.core.helpers.services.in_memory_cache import InMemoryCacheService

router = APIRouter(
    prefix="/pedido",
    tags=["Pedidos"],
)

pedido_command = PedidoServiceCommand(
    OrmPedidoRepository(InMemoryCacheService()),
    OrmPedidoQuery(),
    OrmProductQuery(),
    InMemoryCacheService(),
)


@router.get("/{pedido_id}")
async def get_pedido(pedido_id: int) -> PedidoAggregate:
    try:
        query = PedidoServiceQuery(OrmPedidoQuery())
        return query.get(pedido_id=pedido_id)
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_pedidos(
    status: Annotated[list[int] | None, Query()] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> Union[List[PedidoAggregate], None]:

    try:
        query_options = None
        if any([status, min_value, max_value]):
            query_status = []
            status = status or []
            for s in status:
                query_status.append(CompraStatus(s))
            price_range = structure_value_range(min_value, max_value)
            query_options = PedidoFindOptions(
                status=query_status, price_range=price_range
            )
        query = PedidoServiceQuery(OrmPedidoQuery())
        return query.index(query_options) or []
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_pedido(pedido: CreatePurchaseSchema) -> CompraEntity:
    try:
        purchase = PartialCompraEntity(
            client=PartialClienteEntity(id=pedido.client_id),
            status=CompraStatus.CRIANDO,
            selected_products=None,
            total=PrecoValueObject(
                value=0,
                currency=PartialCurrencyEntity(id=pedido.currency_id),
            ),
        )
        return pedido_command.create_pedido(purchase).purchase
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{pedido_id}/add_product/{product_id}")
async def add_new_product_to_pedido(pedido_id: int, product_id: int) -> CompraEntity:
    try:
        return pedido_command.add_new_product(pedido_id, product_id).purchase
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{pedido_id}/{product_id}/add_component/{component_id}")
async def add_new_component_to_product_in_pedido(
    pedido_id: int, product_id: int, component_id: int
) -> CompraEntity:
    try:
        return pedido_command.add_component_to_select_product(
            pedido_id, product_id, component_id
        ).purchase
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/conclude/{pedido_id}")
async def concludes_pedido(pedido_id: int) -> PedidoAggregate:
    try:
        return pedido_command.concludes_pedido(pedido_id)
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/cancel/{pedido_id}")
async def cancel_pedido(pedido_id: int) -> PedidoAggregate:
    try:
        return pedido_command.cancel_pedido(pedido_id)
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
