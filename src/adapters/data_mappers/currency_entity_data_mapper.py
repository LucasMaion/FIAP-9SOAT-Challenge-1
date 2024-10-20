from src.adapters.driven.infra.models.currencies import Currency
from src.core.domain.entities.currency_entity import PartialCurrencyEntity


class CurrencyEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, currency: Currency):
        return PartialCurrencyEntity(
            id=currency.id,
            name=currency.name,
            symbol=currency.symbol,
            code=currency.code,
            created_at=currency.created_at,
            updated_at=currency.updated_at,
            deleted_at=currency.deleted_at,
        )
