from src.adapters.driven.infra.models.purchases import Purchase
from src.core.domain.entities.compra_entity import PartialCompraEntity


class CompraEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, compra: Purchase):
        return PartialCompraEntity(
            id=compra.id,
            # product_id=compra.product_id,
            status=compra.status,
            total=compra.total_value,
            finalized=compra.finalized,
            canceled=compra.canceled,
            created_at=compra.created_at,
            updated_at=compra.updated_at,
            deleted_at=compra.deleted_at,
        )
