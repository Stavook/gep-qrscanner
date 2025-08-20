import pandas as pd
import traceback
import json 
from typing import List, Union
from pathlib import Path
from .config import WHITELIST_PATH, QR_PATH
from .repository import Repository
from .utils import generate_hash_key, generate_qr_image
from .models import WhitelistEntry

class ExcelRepository(Repository):

    def __init__(self, storage_path = WHITELIST_PATH):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(exist_ok=True, parents=True)

    def generate(self, source: Union[Path, List[WhitelistEntry]]) -> List[WhitelistEntry]:
        
        if isinstance(source, Path):
            df = pd.read_excel(source)
            data_rows = df.iterrows()
        else:
            data_rows = enumerate(source)
        
        whitelist_entries = []
        QR_PATH.mkdir(exist_ok=True, parents=True)

        for idx, row in data_rows:
            #TODO:cleanup this part
            if isinstance(source, Path):
                status = str(row.iloc[9]).strip()  # ΚΑΤΑΣΤΑΣΗ ΔΕΛΤΙΟΥ 
                num = str(row.iloc[0]).strip()   # Α/Α ΔΕΛΤΙΟΥ
                name = str(row.iloc[3]).strip()  # ΕΠΩΝΥΜΟ
            else:
                status = "ΙΣΧΥΕΙ"
                num = row.num
                name = row.surname
            
            if status != "ΙΣΧΥΕΙ":
                continue
            
            if not num or not name:
                continue

            try:
                hash_key = generate_hash_key(num, name)
                qr_filename = f"{num}-{name}.png"
                qr_path = QR_PATH / qr_filename
                generate_qr_image(hash_key, qr_path)
            except Exception:
                traceback.print_exc()
                continue
            
            entry = WhitelistEntry(
                num=num,
                surname=name,
                qr_data=hash_key,
                qr_image_path=str(qr_path)
            )
            whitelist_entries.append(entry)

        return whitelist_entries
    
    def save(self, entries: List[WhitelistEntry]) -> None:
        try:
            entries_dict = [entry.dict() for entry in entries]
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(entries_dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving entries: {e}")
            raise

    def load(self) -> List[WhitelistEntry]:
        try:
            if not self.storage_path.exists():
                return []
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                entries_dict = json.load(f)
            
            return [WhitelistEntry(**entry_dict) for entry_dict in entries_dict]

        except Exception as e:
            print(f"Error loading entries: {e}")
            return []

    