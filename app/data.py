from abc import ABC, abstractmethod
from typing import Dict, Optional

from redis import Redis


class DataStore(ABC):

    @abstractmethod
    def add_redirect(self, src: str, target: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_target(self, src: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def has_redirect(self, src: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_redirect(self, src: str) -> bool:
        raise NotImplementedError


class MemoryDataStore(DataStore):

    def __init__(self):
        self.redirects: Dict[str, str] = {}

    def add_redirect(self, src: str, target: str) -> None:
        self.redirects[src] = target

    def get_target(self, src: str) -> Optional[str]:
        return self.redirects.get(src)

    def has_redirect(self, src: str) -> bool:
        return src in self.redirects

    def delete_redirect(self, src: str) -> bool:
        target = self.redirects.pop(src, None)
        return target is not None


class RedisDataStore(DataStore):

    def __init__(self, **kwargs):
        self.r = Redis(**kwargs)

    def add_redirect(self, src: str, target: str) -> None:
        self.r.set(src, target)

    def get_target(self, src: str) -> Optional[str]:
        return self.r.get(src)

    def has_redirect(self, src: str) -> bool:
        return self.r.exists(src)

    def delete_redirect(self, src: str) -> bool:
        return self.r.delete(src)
