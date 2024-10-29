from src.core.application.interfaces.produto_command import IProductCommand
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class ProductServiceCommand(IProductCommand):

    def create_product(self, produto: PartialProdutoEntity) -> ProdutoAggregate:
        if not isinstance(produto, PartialProdutoEntity):
            raise TypeError("produto must be an instance of PartialProdutoEntity")
        options = ProdutoFindOptions(
            name=produto.name,
        )
        existing_products = self.product_query.find(options)
        if existing_products:
            raise ValueError("Já existe um produto com esse nome")
        produto.is_active = False
        return self.product_repository.create(produto)

    def activate_product(self, product_id: int) -> ProdutoAggregate:
        product = self.product_query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")
        product = product.product
        if not product:
            raise ValueError("Produto não encontrado")
        if product.is_active:
            raise ValueError("Produto já está ativo")
        if product.category is None:
            raise ValueError("Produto não possui categoria")
        if product.price is None:
            raise ValueError("Produto não possui preço")
        product.is_active = True
        return self.product_repository.update(product)

    def deactivate_product(self, product_id: int) -> ProdutoEntity:
        product = self.product_query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")
        product = product.product
        if product.is_active is False:
            raise ValueError("Produto já está inativo")
        product.is_active = False
        return self.product_repository.update(product)

    def delete_product(self, product_id: int):
        product_aggregate = self.product_repository.get_by_product_id(product_id)
        if not product_aggregate:
            raise ValueError("Produto não encontrado")
        if product_aggregate.product.is_active:
            raise ValueError("Produto ativo, impossível deletar!")
        if product_aggregate.orders:
            raise ValueError("Produto possui pedidos associados, impossível deletar!")
        self.product_repository.delete(product_id)

    def update_product(self, produto: ProdutoEntity) -> ProdutoEntity:
        current_product = self.product_query.get(produto.id)
        if not current_product:
            raise ValueError("Produto não encontrado")
        current_product = current_product.product
        produto.is_active = current_product.is_active
        if produto.price.value < 0:
            raise ValueError("Preço não pode ser negativo")
        if produto.price.value == 0:
            raise ValueError("Preço não pode ser zero")

        if current_product.name != produto.name:
            if self.product_query.find(
                query_options=ProdutoFindOptions(name=produto.name)
            ):
                raise ValueError("Já existe um produto com esse nome")

        if current_product.category != produto.category:
            if not self.category_query.get(current_product.category.id):
                raise ValueError("Categoria não encontrada")
        if produto.allow_components and produto.category.is_component:
            raise ValueError("Um Acompanhamento não permite ter outros acompanhamentos")
        if not produto.allow_components and produto.components:
            raise ValueError(
                "Produto não permite acompanhamentos, mas possui acompanhamentos"
            )
        if produto.components:
            seen = set()
            duplicates = []

            for x in produto.components:
                if x.id in seen:
                    duplicates.append(x.id)
                else:
                    seen.add(x.id)
            if duplicates:
                raise ValueError("Acompanhamentos não podem ser duplicados")
            new_component_ids = list(
                set([comp.id for comp in produto.components])
                - set([comp.id for comp in current_product.components])
            )
            if produto.id in new_component_ids:
                raise ValueError("Um produto não pode ser componente de si mesmo")
            for new_component_id in new_component_ids:
                component = self.product_query.get_only_entity(new_component_id)
                if not component:
                    raise ValueError("Acompanhamento não encontrado")
                if not component.category.is_component:
                    raise ValueError(
                        "Apenas produtos do tipo 'Acompanhamento' podem ser acompanhamentos"
                    )
        return self.product_repository.update(produto)
