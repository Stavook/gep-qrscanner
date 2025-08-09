import logging
import traceback
from typing import Set
import pandas as pd
from pathlib import Path
from .utils import generate_hash_key, generate_qr_image
from .repository_excel import ExcelWhitelistRepository
from .config import QR_PATH

class WhitelistService:
    def __init__(self, repository=None):
        self.repository = repository or ExcelWhitelistRepository()

    def load_whitelist(self) -> Set[str]:
        self.whitelist = self.repository.load()
        return self.whitelist

    def is_valid(self, qr_data: str) -> bool:
        return qr_data in self.whitelist

    def save_entries(self, entries: list[dict]):
        self.repository.save(entries)
        self.load_whitelist()  

    def generate_whitelist(self, path: Path):
        df = pd.read_excel(path)
        whitelist_entries = []

        QR_PATH.mkdir(exist_ok=True, parents=True)

        for idx, row in df.iterrows():
            status = str(row.iloc[9]).strip()  # ΚΑΤΑΣΤΑΣΗ ΔΕΛΤΙΟΥ 
            if status != "ΙΣΧΥΕΙ":
                logging.info(f"Skipping row {idx} — ΚΑΤΑΣΤΑΣΗ ΔΕΛΤΙΟΥ: '{status}'")
                continue
            
            num = str(row.iloc[0]).strip()   # Α/Α ΔΕΛΤΙΟΥ
            name = str(row.iloc[3]).strip()  # ΕΠΩΝΥΜΟ
            
            if not num or not name:
                logging.warning(f"Skipping row {idx} — missing Α/Α ΔΕΛΤΙΟΥ or ΕΠΩΝΥΜΟ")
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

        self.save_entries(whitelist_entries)
        logging.info("Finished generating QR codes and creating whitelist")
    
