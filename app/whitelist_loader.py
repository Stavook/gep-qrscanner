import pandas as pd
from app.config import WHITELIST_PATH

def load_whitelist(path=WHITELIST_PATH):
    try:
        df = pd.read_excel(path)
        return set(df['qr_data'].dropna().astype(str))
    except Exception as e:
        print(f"Error loading whitelist: {e}")
        return set()
