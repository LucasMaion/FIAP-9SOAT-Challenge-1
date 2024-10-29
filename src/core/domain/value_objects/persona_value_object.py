from datetime import datetime
import re
from typing import Optional

from pydantic import field_validator
from src.core.domain.base.value_object import ValueObject
from src.core.domain.value_objects.address_value_object import AddressValueObject


class PersonaValueObject(ValueObject):
    name: str
    document: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    address: Optional[AddressValueObject] = None

    @field_validator("document")
    def validate_cpf(cls, document):
        cpf_pattern = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
        if not cpf_pattern.match(document):
            raise ValueError("CPF Inválido.")
        return document

    @field_validator("email")
    def validate_email(cls, email):
        email_pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
        if not email_pattern.match(email):
            raise ValueError("Email Inválido.")

    @field_validator("phone")
    def validate_ehone(cls, phone):
        phone_pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
        if not phone_pattern.match(phone):
            raise ValueError("Telefone Inválido.")
