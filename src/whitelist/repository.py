from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from pathlib import Path

class Repository(ABC):

    @abstractmethod
    def load(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def save(self, entries: List[Dict[str, str]]) -> None:
        pass

    @abstractmethod
    def generate(self, source: Union[Path, List[Dict[Any, Any]]]) -> List[Dict[str, str]]:
        pass