from typing import List,Dict,Union,Set
from pathlib import Path
from .repository import Repository
from .models import WhitelistEntry

class WhitelistService:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.whitelist: Set[str] = set()
        self.load_whitelist()
    
    def is_valid(self, qr_data: str) -> bool:
        return qr_data in self.whitelist

    def save_entries(self, entries: List[WhitelistEntry]) -> None:
        self.repository.save(entries)
        self.load_whitelist()
    
    def generate(self, source: Union[Path, List[WhitelistEntry]]) -> List[WhitelistEntry]:
        entries = self.repository.generate(source)
        self.save_entries(entries)
        return entries

    def load_whitelist(self) -> None:
        try:
            entries = self.repository.load()
            self.whitelist = {
                entry.qr_data 
                for entry in entries 
                if entry.qr_data
            }
            print(f"Loaded {len(self.whitelist)} entries into whitelist")
        except Exception as e:
            print(f"Error loading whitelist: {e}")
            self.whitelist = set()
    
    def get_entries(self) -> List[WhitelistEntry]:
        return self.repository.load()
    
    def get_entry_by_qr(self, qr_data: str) -> WhitelistEntry | None:
        entries = self.repository.load()
        for entry in entries:
            if entry.qr_data == qr_data:
                return entry
        return None
    
    def get_whitelist_stats(self) -> Dict[str, int]:
        entries = self.repository.load()
        return {
            "total_entries": len(entries),
            "active_qr_codes": len(self.whitelist)
        }



