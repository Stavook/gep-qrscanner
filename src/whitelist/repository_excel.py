# src/whitelist/repository_excel.py
import pandas as pd
from typing import Set
from .config import WHITELIST_PATH
from .repository import WhitelistRepository

class ExcelWhitelistRepository(WhitelistRepository):

    def load(self) -> Set[str]:
        if not WHITELIST_PATH.exists():
            return set()
        df = pd.read_excel(WHITELIST_PATH)
        return set(df['qr_data'].dropna().astype(str))

    def save(self, entries: list[dict]):
        WHITELIST_PATH.parent.mkdir(exist_ok=True, parents=True)
        df = pd.DataFrame(entries)
        if WHITELIST_PATH.exists():
            existing_df = pd.read_excel(WHITELIST_PATH)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df = updated_df.drop_duplicates(subset=["qr_data"])
            updated_df.to_excel(WHITELIST_PATH, index=False)
        else:
            df = df.drop_duplicates(subset=["qr_data"])
            df.to_excel(WHITELIST_PATH, index=False)
