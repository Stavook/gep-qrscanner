from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from pathlib import Path
from .models import WhitelistEntry

class Repository(ABC):

    @abstractmethod
    def load(self) -> List[WhitelistEntry]:
        pass

    @abstractmethod
    def save(self, entries: List[WhitelistEntry]) -> None:
        pass

    @abstractmethod
    def generate(self, source: Union[Path, List[WhitelistEntry]]) -> List[WhitelistEntry]:
        pass