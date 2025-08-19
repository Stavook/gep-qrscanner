import pandas as pd
import traceback
import json 
from typing import List, Dict, Union, Any
from pathlib import Path
from .config import WHITELIST_PATH, QR_PATH
from .repository import Repository
from .utils import generate_hash_key, generate_qr_image

class ExcelRepository(Repository):

    def __init__(self, storage_path = WHITELIST_PATH):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(exist_ok=True, parents=True)

    def generate(self, source: Union[Path, List[Dict[Any, Any]]]) -> List[Dict[str, str]]:
        
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
                status = str(row.get('status', '')).strip()
                num = str(row.get('id', row.get('num', ''))).strip()
                name = str(row.get('name', '')).strip()
            
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

            entry = {
                "Α/Α ΔΕΛΤΙΟΥ": num,
                "ΕΠΩΝΥΜΟ": name,
                "qr_data": hash_key,
                "qr_image": str(qr_path)
            }
            whitelist_entries.append(entry)

        return whitelist_entries
    
    def save(self, entries: List[Dict[str, str]]) -> None:
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving entries: {e}")
            raise

    def load(self) -> List[Dict[str,str]]:
        try:
            if not self.storage_path.exists():
                return []
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading entries: {e}")
            return []

    