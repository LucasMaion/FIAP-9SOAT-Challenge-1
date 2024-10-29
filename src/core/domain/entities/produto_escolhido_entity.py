from typing import List, Optional

from src.core.domain.base.entity import Entity, PartialEntity
from src.core.domain.entities.produto_entity import ProdutoEntity


class ProdutoEscolhidoEntity(Entity):
    product: ProdutoEntity
    added_components: Optional[List[ProdutoEntity]] = None


class PartialProdutoEscolhidoEntity(PartialEntity, ProdutoEscolhidoEntity):
    product: ProdutoEntity = None
