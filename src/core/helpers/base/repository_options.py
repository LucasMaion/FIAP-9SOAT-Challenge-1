from abc import ABC
from typing import Optional

from pydantic import BaseModel


class RepositoryOptions(BaseModel, ABC):
    id: Optional[int] = None
