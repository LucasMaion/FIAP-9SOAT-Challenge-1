from typing import List, Union
from fastapi import APIRouter, HTTPException
from loguru import logger

from src.adapters.driven.infra.ports.orm_pedido_query import OrmPedidoQuery
from src.adapters.driven.infra.ports.orm_produto_query import OrmProductQuery
from src.adapters.driven.infra.repositories.orm_pedido_repository import (
    OrmPedidoRepository,
)
from src.core.application.services.pedido_service_command import PedidoServiceCommand
from src.core.application.services.pedido_service_query import PedidoServiceQuery
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.options.pedido_find_options import PedidoFindOptions
from src.core.helpers.services.in_memory_cache import InMemoryCacheService

router = APIRouter(
    prefix="/queue",
    tags=["Fila de Pedidos"],
)

pedido_command = PedidoServiceCommand(
    OrmPedidoRepository(InMemoryCacheService()),
    OrmPedidoQuery(),
    OrmProductQuery(),
    InMemoryCacheService(),
)


@router.get("/")
async def get_queue() -> Union[List[PedidoAggregate], None]:
    try:
        query = PedidoServiceQuery(OrmPedidoQuery())
        query_options = PedidoFindOptions(
            status=(
                CompraStatus.CONCLUIDO,
                CompraStatus.EM_PREPARO,
                CompraStatus.PRONTO_PARA_ENTREGA,
                CompraStatus.ENTREGUE,
            )
        )

        return query.index(query_options) or []
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/")
async def update_queue_item_status(
    pedido_id: int, new_status_number: int
) -> PedidoAggregate:
    try:
        return pedido_command.update_status(
            pedido_id=pedido_id, new_status=CompraStatus(new_status_number)
        )
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
