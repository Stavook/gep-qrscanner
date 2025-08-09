from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from .whitelist.service import WhitelistService
from .whitelist.models import QrValidationRequest
from .whitelist.config import WHITELIST_PATH


app = FastAPI()
whitelist_service = WhitelistService()
whitelist_service.load_whitelist()


@app.post("/validate_qr")
def validate_qr(payload: QrValidationRequest):
    valid = whitelist_service.is_valid(payload.qr_data)
    return {"qr_data": payload.qr_data, "valid": valid}

@app.post("/reload_whitelist/")
def reload_whitelist():
    whitelist_service.load_whitelist()
    return {"message": "Whitelist reloaded"}

@app.post("/upload_whitelist/")
def upload_whitelist(file: UploadFile = File(...)):
    with open(WHITELIST_PATH, "wb") as f:
        f.write(file.file.read())
    whitelist_service.load_whitelist()
    return {"message": "Whitelist uploaded and reloaded"}

@app.post("/generate_whitelist/")
async def generate_whitelist(file: UploadFile = File(...)):
    temp_path = Path("temp_uploaded.xlsx")
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    whitelist_service.generate_whitelist(temp_path)
    temp_path.unlink()
    
    return {"message": "Whitelist generated from uploaded Excel"}