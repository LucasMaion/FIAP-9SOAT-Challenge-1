from typing import List, Optional
from src.core.domain.base.entity import Entity, PartialEntity
from src.core.domain.entities.cliente_entity import ClienteEntity
from src.core.domain.entities.produto_escolhido_entity import ProdutoEscolhidoEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.compra_status import CompraStatus


class CompraEntity(Entity):
    client: ClienteEntity
    status: CompraStatus
    selected_products: List[ProdutoEscolhidoEntity]
    total: PrecoValueObject


class PartialCompraEntity(PartialEntity, CompraEntity):
    client: Optional[ClienteEntity] = None
    status: Optional[CompraStatus] = None
    selected_products: Optional[List[ProdutoEscolhidoEntity]] = None
    total: Optional[PrecoValueObject] = None
