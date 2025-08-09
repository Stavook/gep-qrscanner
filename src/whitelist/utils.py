from hashlib import sha256
import qrcode as qr
from pathlib import Path

def generate_qr_image(hash: str, path: Path):    
        qr_image = qr.make(hash, image_factory = None)
        path.parent.mkdir(parents = True, exist_ok= True)
        qr_image.save(str(path))

def generate_hash_key(aa : str, name : str) -> str:
    input_str = f"{aa.strip()}-{name.lower().strip()}"
    return sha256(input_str.encode('utf-8')).hexdigest()