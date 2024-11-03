from typing import Optional
from src.core.helpers.base.repository_options import RepositoryOptions


class ClientFindOptions(RepositoryOptions):
    email: Optional[str] = None
    document: Optional[str] = None
    name: Optional[str] = None
