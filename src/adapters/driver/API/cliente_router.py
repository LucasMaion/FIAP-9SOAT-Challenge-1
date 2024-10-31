from typing import Union
from fastapi import APIRouter, HTTPException
from loguru import logger
from src.adapters.driven.infra.ports.orm_cliente_query import OrmClienteQuery
from src.adapters.driven.infra.repositories.orm_client_repository import (
    OrmClientRepository,
)
from src.adapters.driver.API.schemas.create_client_schema import CreateClientSchema
from src.core.application.services.cliente_service import ClienteCommand
from src.core.domain.aggregates.cliente_aggregate import ClienteAggregate
from src.core.domain.entities.cliente_entity import PartialClienteEntity
from src.core.domain.value_objects.persona_value_object import PersonaValueObject

router = APIRouter(
    prefix="/cliente",
    tags=["Clientes"],
)


@router.get("/{document}")
async def get_item_by_document(document: str) -> Union[ClienteAggregate, None]:
    try:
        service = ClienteCommand(OrmClientRepository(), OrmClienteQuery())
        result = service.get_client_by_document(document)
        return result
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=201)
async def create_client(
    new_client: CreateClientSchema,
) -> Union[ClienteAggregate, None]:
    try:
        service = ClienteCommand(OrmClientRepository(), OrmClienteQuery())
        client: PartialClienteEntity = PartialClienteEntity(
            person=PersonaValueObject(
                name=new_client.name,
                document=new_client.document,
                email=new_client.email,
            )
        )
        result = service.create_client(client)
        return result
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
