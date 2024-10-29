from src.core.application.interfaces.pedido_command import IPedidoCommand
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.entities.produto_escolhido_entity import (
    PartialProdutoEscolhidoEntity,
)
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.enums.pagamento_status import PagamentoStatus


class PedidoCommand(IPedidoCommand):
    def create_pedido(self, pedido: PartialCompraEntity) -> PedidoAggregate:
        return self.purchase_repository.create_compra(pedido)

    def concludes_pedido(self, pedido_id: int) -> PedidoAggregate:
        pedido = self.purchase_query.get(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado.")
        if pedido.purchase.status == CompraStatus.CONCLUIDO:
            raise ValueError("Pedido não possui pagamento efetuado.")
        if not pedido.purchase.selected_products:
            raise ValueError("Pedido não possui produtos.")
        if not pedido.payment or pedido.payment.status != PagamentoStatus.PAGO:
            raise ValueError("Pedido não possui pagamento efetuado.")
        if pedido.purchase.total.value == 0:
            raise ValueError("Valor do pedido é zero.")
        if pedido.purchase.total.value < 0:
            raise ValueError("Valor do pedido é negativo.")
        return self._execute_update_status(pedido, CompraStatus.CONCLUIDO)

    def cancel_pedido(self, pedido_id: int) -> PedidoAggregate:
        pedido = self.purchase_query.get(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado.")
        return self._execute_update_status(pedido, CompraStatus.CANCELADO)

    def add_new_product(self, pedido_id: int, product_id: int):
        pedido = self.purchase_query.get(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        produto = self.produto_query.get_only_entity(product_id)
        if not produto:
            raise ValueError("Produto não encontrado")
        selected_product = PartialProdutoEscolhidoEntity(
            product=produto, added_components=[]
        )
        pedido.purchase.selected_products.append(selected_product)
        pedido.purchase.total.value = self._calculate_total_value(pedido.purchase)
        return self.purchase_repository.update_compra(pedido.purchase)

    def remove_select_product(self, pedido_id: int, selected_product_id: int):
        pedido = self.purchase_query.get(pedido_id)
        current_length = len(pedido.purchase.selected_products)
        pedido.purchase.selected_products = [
            selected_product
            for selected_product in pedido.purchase.selected_products
            if selected_product.id != selected_product_id
        ]
        if current_length == len(pedido.purchase.selected_products):
            raise ValueError("Produto não está no pedido.")
        pedido.purchase.total.value = self._calculate_total_value(pedido.purchase)
        return self.purchase_repository.update_compra(pedido.purchase)

    def add_component_to_select_product(
        self, pedido_id: int, selected_product_id: int, component_id: int
    ):
        pedido = self.purchase_query.get(pedido_id)
        adding_product = self.produto_query.get_only_entity(selected_product_id)
        if not any(
            component
            for component in adding_product.components
            if component.id == component_id
        ):
            raise ValueError("Produto não possui esse adicional.")
        new_component = self.produto_query.get_only_entity(component_id)
        target_selected_product = next(
            (
                selected_product
                for selected_product in pedido.purchase.selected_products
                if selected_product.id == selected_product_id
            ),
            None,
        )
        if not target_selected_product:
            raise ValueError("Selected product not found")
        target_selected_product.added_components.append(new_component)
        pedido.purchase.total.value = self._calculate_total_value(pedido.purchase)
        return self.purchase_repository.update_compra(pedido.purchase)

    def update_status(
        self, pedido_id: int, new_status: CompraStatus
    ) -> PedidoAggregate:
        pedido = self.purchase_query.get(pedido_id)
        return self._execute_update_status(pedido, new_status)

    def _execute_update_status(
        self, pedido: CompraEntity, new_status: CompraStatus
    ) -> PedidoAggregate:
        if not self._pedido_state_machine(pedido.purchase.status, new_status):
            raise ValueError(
                f"Não é permitido mudar do status {pedido.purchase.status.name} para o status {new_status.name}"
            )
        pedido.purchase.status = new_status
        return self.purchase_repository.update_compra(pedido.purchase)

    def _calculate_total_value(self, compra: CompraEntity):
        total = 0
        for selected_product in compra.selected_products:
            total += selected_product.product.price.value
            for component in selected_product.added_components:
                total += component.price.value
        return total

    @staticmethod
    def _pedido_state_machine(current_status: CompraStatus, new_status: CompraStatus):
        match current_status:
            case CompraStatus.CRIANDO:
                if new_status in (CompraStatus.CRIANDO,):
                    return False
                return True
            case CompraStatus.PAGO:
                if new_status in (CompraStatus.CRIANDO, CompraStatus.PAGO):
                    return False
                return True
            case CompraStatus.CANCELADO:
                # Cancelado não pode mudar de status
                return False
            case CompraStatus.CONCLUIDO:
                if new_status in (
                    CompraStatus.CRIANDO,
                    CompraStatus.PAGO,
                    CompraStatus.CONCLUIDO,
                ):
                    return False
                return True
            case CompraStatus.EM_PREPARO:
                if new_status in (
                    CompraStatus.CRIANDO,
                    CompraStatus.PAGO,
                    CompraStatus.CONCLUIDO,
                    CompraStatus.EM_PREPARO,
                ):
                    return False
                return True
            case CompraStatus.PRONTO_PARA_ENTREGA:
                if new_status in (
                    CompraStatus.CRIANDO,
                    CompraStatus.PAGO,
                    CompraStatus.CONCLUIDO,
                    CompraStatus.EM_PREPARO,
                    CompraStatus.PRONTO_PARA_ENTREGA,
                ):
                    return False
                return True
            case CompraStatus.ENTREGUE:
                if new_status in (
                    CompraStatus.CRIANDO,
                    CompraStatus.PAGO,
                    CompraStatus.CONCLUIDO,
                    CompraStatus.EM_PREPARO,
                    CompraStatus.PRONTO_PARA_ENTREGA,
                    CompraStatus.ENTREGUE,
                ):
                    return False
                return True
            case CompraStatus.FINALIZADO:
                # Finalizado não pode mudar de status
                return False
            case _:
                return False
