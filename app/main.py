from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.whitelist_validator import is_valid_qr, reload_list
from app.whitelist_loader import load_list
from app.config import WHITELIST_PATH

app = FastAPI()

class QrValidationRequest(BaseModel):
    qr_data: str
# class QrValidationResponse

@app.post("/validate_qr")
def validate_qr(payload: QrValidationRequest):
    valid = is_valid_qr(payload.qr_data)
    # if valid:
    return {"qr_data": payload.qr_data, "valid": valid}
    
@app.post("/reload_whitelist/")
def reload_whitelist():
    reload_list()
    return {"message": "Whitelist reloaded"}

@app.post("/upload_whitelist/")
def upload_whitelist(file: UploadFile = File(...)):
    with open(WHITELIST_PATH, "wb") as f:
        f.write(file.file.read())
    reload_whitelist()
    return {"message": "Whitelist uploaded and reloaded"}

