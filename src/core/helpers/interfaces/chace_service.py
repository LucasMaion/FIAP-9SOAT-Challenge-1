from abc import ABC, abstractmethod


class CacheService(ABC):
    @abstractmethod
    def set(self, key: str, value: any, ttl: int = 300) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> any:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
