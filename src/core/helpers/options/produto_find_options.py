from typing import Optional, Tuple
from src.core.helpers.base.repository_options import RepositoryOptions


class ProdutoFindOptions(RepositoryOptions):
    name: Optional[str] = None
    category: Optional[str] = None
    price_range: Optional[Tuple[Optional[float], Optional[float]]] = None
