from pydantic import BaseModel
from typing import Optional

class WhitelistEntry(BaseModel):
    num: str
    surname: str  
    qr_data: str
    qr_image_path: str

class QrValidationResponse(BaseModel):
    qr_data: str
    valid: bool
    entry: Optional[WhitelistEntry] = None

class QrValidationRequest(BaseModel):
    qr_data: str
    