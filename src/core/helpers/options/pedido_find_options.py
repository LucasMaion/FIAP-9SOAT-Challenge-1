from datetime import datetime
from typing import List, Optional, Tuple
from src.core.helpers.base.repository_options import RepositoryOptions
from src.core.helpers.enums.compra_status import CompraStatus


class PedidoFindOptions(RepositoryOptions):
    status: Optional[List[CompraStatus]] = None
    total_value_range: Optional[Tuple[Optional[float], Optional[float]]] = None
