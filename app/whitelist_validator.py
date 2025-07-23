from app.whitelist_loader import load

whitelist = load()

def is_valid_qr(qr_data: str) -> bool:
    return qr_data in whitelist

def reload():
    global whitelist
    whitelist = load()
