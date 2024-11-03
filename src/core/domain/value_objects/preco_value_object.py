from decimal import Decimal

from src.core.domain.base.value_object import ValueObject
from src.core.domain.entities.currency_entity import CurrencyEntity


class PrecoValueObject(ValueObject):
    value: Decimal
    currency: CurrencyEntity
