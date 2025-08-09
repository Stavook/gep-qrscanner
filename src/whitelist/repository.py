from abc import ABC, abstractmethod
from typing import Set

class WhitelistRepository(ABC):

    @abstractmethod
    def load(self) -> Set[str]:
        pass

    @abstractmethod
    def save(self, entries: list[dict]):
        pass
