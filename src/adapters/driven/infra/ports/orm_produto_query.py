from peewee import JOIN
from typing import List, Union
from src.adapters.data_mappers.produto_aggregate_data_mapper import (
    ProdutoAggregateDataMapper,
)
from src.adapters.data_mappers.produto_entity_data_mapper import ProdutoEntityDataMapper
from src.adapters.driven.infra.models.categories import Category
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.product_components import ProductComponent
from src.adapters.driven.infra.models.products import Product
from src.core.application.ports.produto_query import ProdutoQuery
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.produto_entity import ProdutoEntity
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class OrmProductQuery(ProdutoQuery):
    def get_only_entity(self, item_id: int) -> Union[ProdutoEntity, None]:
        product: Product = (
            Product.select()
            .join(
                Category,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                ProductComponent,
                on=(ProductComponent.product == Product.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                Currency,
                join_type=JOIN.LEFT_OUTER,
            )
            .where(Product.id == item_id)
        )
        parsed_result = [
            ProdutoEntityDataMapper.from_db_to_domain(res) for res in product
        ]
        if not parsed_result:
            return None
        return parsed_result[0]

    def get(self, item_id: int) -> Union[ProdutoAggregate, None]:
        product: Product = (
            Product.select()
            .join(
                Category,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                ProductComponent,
                on=(ProductComponent.product == Product.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                Currency,
                join_type=JOIN.LEFT_OUTER,
            )
            .where(Product.id == item_id)
        )
        parsed_result = [
            ProdutoAggregateDataMapper.from_db_to_domain(res) for res in product
        ]
        if not parsed_result:
            return None
        return parsed_result[0]

    def get_all(self) -> List[ProdutoAggregate]:
        result: Product = (
            Product.select()
            .join(
                Category,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                ProductComponent,
                on=(ProductComponent.product == Product.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                Currency,
                join_type=JOIN.LEFT_OUTER,
            )
        )
        parsed_result = [
            ProdutoAggregateDataMapper.from_db_to_domain(res) for res in result
        ]
        return parsed_result

    def find(self, query_options: ProdutoFindOptions) -> List[ProdutoAggregate]:
        queries = []
        if query_options.name:
            queries.append(Product.name.contains(query_options.name))
        if query_options.category:
            queries.append(Category.name.contains(query_options.category))
        if query_options.price_range:
            queries.append(Product.price.between(*query_options.price_range))

        result = (
            Product.select()
            .join(
                Currency,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                Category,
                join_type=JOIN.LEFT_OUTER,
            )
            .switch(Product)
            .join(
                ProductComponent,
                on=(ProductComponent.product == Product.id),
                join_type=JOIN.LEFT_OUTER,
            )
            .where(*queries)
        )
        parsed_result = [
            ProdutoAggregateDataMapper.from_db_to_domain(res) for res in result
        ]
        return parsed_result
