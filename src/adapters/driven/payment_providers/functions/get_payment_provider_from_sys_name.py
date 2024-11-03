from typing import Type
from src.adapters.driven.payment_providers.interfaces.payment_provider import (
    PaymentProvider,
)
from src.adapters.driven.payment_providers import providers


def get_payment_provider_from_sys_name(sys_name: str) -> Type[PaymentProvider]:
    if hasattr(providers, sys_name):
        return getattr(providers, sys_name)
    raise NotImplementedError(f"Payment provider '{sys_name}' not found.")
