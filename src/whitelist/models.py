from pydantic import BaseModel

class QrValidationRequest(BaseModel):
    qr_data: str
    
class WhitelistEntry(BaseModel):
    num: str
    surname: str
    qr_data: str
    qr_image_path: str