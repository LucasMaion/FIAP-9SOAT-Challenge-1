from typing import Optional

from src.core.domain.base.value_object import ValueObject


class AddressValueObject(ValueObject):
    zip_code: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    additional_information: Optional[str] = None
