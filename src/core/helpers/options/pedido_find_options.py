from datetime import datetime
from typing import Optional, Tuple
from src.core.helpers.base.repository_options import RepositoryOptions


class PedidoFindOptions(RepositoryOptions):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price_range: Optional[Tuple[Optional[float], Optional[float]]] = None
    created_at: Optional[datetime] = None
