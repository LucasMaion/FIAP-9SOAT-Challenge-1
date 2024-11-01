from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException
from loguru import logger
from src.adapters.driven.infra.ports.orm_categoria_query import OrmCategoriaQuery
from src.adapters.driven.infra.ports.orm_currency_query import OrmCurrencyQuery
from src.adapters.driven.infra.ports.orm_produto_query import OrmProductQuery
from src.adapters.driven.infra.repositories.orm_produto_repository import (
    OrmProdutoRepository,
)
from src.adapters.driver.API.schemas.create_product_schema import CreateProductSchema
from src.adapters.driver.API.schemas.update_product_schema import UpdateProductSchema
from src.core.application.services.produto_service_command import ProductServiceCommand
from src.core.application.services.produto_service_query import (
    ProdutoServiceQuery,
)
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.categoria_entity import (
    CategoriaEntity,
    PartialCategoriaEntity,
)
from src.core.domain.entities.currency_entity import (
    PartialCurrencyEntity,
)
from src.core.domain.entities.produto_entity import PartialProdutoEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.functions.structure_value_range import structure_value_range
from src.core.helpers.options.produto_find_options import ProdutoFindOptions

router = APIRouter(
    prefix="/produto",
    tags=["Produtos"],
)


@router.get("/categories")
async def list_categories() -> Union[List[CategoriaEntity], None]:
    try:
        query = ProdutoServiceQuery(
            OrmProductQuery(), OrmCategoriaQuery(), OrmCurrencyQuery()
        )
        return query.list_categories()
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index")
async def list_itens(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> Union[List[ProdutoAggregate], None]:
    try:
        query = ProdutoServiceQuery(
            OrmProductQuery(), OrmCategoriaQuery(), OrmCurrencyQuery()
        )
        query_options = None
        if any([name, category, min_price, max_price]):
            price_range = structure_value_range(min_price, max_price)
            query_options = ProdutoFindOptions(
                name=name, category=category, price_range=price_range
            )
        return query.index(query_options)
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}")
async def get_item(item_id: int) -> Union[ProdutoAggregate, None]:
    try:
        query = ProdutoServiceQuery(
            OrmProductQuery(), OrmCategoriaQuery(), OrmCurrencyQuery()
        )
        result = query.get(item_id)
        return result
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=201)
async def create_item(produto: CreateProductSchema) -> ProdutoAggregate:
    try:
        command = ProductServiceCommand(
            OrmProdutoRepository(),
            OrmProductQuery(),
            OrmCategoriaQuery(),
            OrmCurrencyQuery(),
        )
        product = PartialProdutoEntity(
            name=produto.name,
            allow_components=produto.allow_components,
            price=PrecoValueObject(
                value=produto.value,
                currency=PartialCurrencyEntity(id=produto.currency_id),
            ),
            category=PartialCategoriaEntity(id=produto.category_id),
        )
        result = command.create_product(product)
        return result
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/")
async def update_item(produto: UpdateProductSchema) -> ProdutoAggregate:
    try:
        command = ProductServiceCommand(
            OrmProdutoRepository(),
            OrmProductQuery(),
            OrmCategoriaQuery(),
            OrmCurrencyQuery(),
        )
        product = PartialProdutoEntity(
            id=produto.id,
            name=produto.name,
            allow_components=produto.allow_components,
            price=PrecoValueObject(
                value=produto.value,
                currency=PartialCurrencyEntity(id=produto.currency_id),
            ),
            category=PartialCategoriaEntity(id=produto.category_id),
            components=[
                PartialProdutoEntity(id=component_id)
                for component_id in produto.component_ids
            ],
        )
        return command.update_product(product)
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    try:
        command = ProductServiceCommand(
            OrmProdutoRepository(),
            OrmProductQuery(),
            OrmCategoriaQuery(),
            OrmCurrencyQuery(),
        )
        command.delete_product(item_id)
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/activate/{item_id}")
async def activate_item(item_id: int) -> ProdutoAggregate:
    command = ProductServiceCommand(
        OrmProdutoRepository(),
        OrmProductQuery(),
        OrmCategoriaQuery(),
        OrmCurrencyQuery(),
    )
    return command.activate_product(item_id)


@router.patch("/deactivate/{item_id}")
async def deactivate_item(item_id: int) -> ProdutoAggregate:
    command = ProductServiceCommand(
        OrmProdutoRepository(),
        OrmProductQuery(),
        OrmCategoriaQuery(),
        OrmCurrencyQuery(),
    )
    return command.deactivate_product(item_id)
