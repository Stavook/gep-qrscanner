from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from typing import Dict, Any, List
from .service import WhitelistService
from .models import QrValidationRequest, QrValidationResponse, WhitelistEntry
from .repository_excel import ExcelRepository 
from .config import WHITELIST_PATH

router = APIRouter()

excel_repository = ExcelRepository(WHITELIST_PATH)
whitelist_service = WhitelistService(excel_repository)

@router.post("/validate_qr/", response_model = QrValidationResponse)
def validate_qr(payload: QrValidationRequest) -> QrValidationResponse:
    try:
        valid = whitelist_service.is_valid(payload.qr_data)
        entry = None
    
        if valid:
            entry = whitelist_service.get_entry_by_qr(payload.qr_data)
        return QrValidationResponse(
            qr_data = payload.qr_data,
            valid = valid,
            entry = entry
        )

    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Validation error: {str(e)}")

@router.post("/reload/")
def reload_whitelist() -> Dict[str, Any]:
    try:
        whitelist_service.load_whitelist()
        stats = whitelist_service.get_whitelist_stats()
        return {
            "message": "Whitelist reloaded",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Reload error: {str(e)}")
 

@router.post("/upload/")
async def upload_whitelist(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Only JSON files are accepted")
    
    try:
        temp_path = Path(f"temp_{file.filename}")
        content = await file.read()
        
        with open(temp_path, "wb") as f:
            f.write(content)
        
        import json
        with open(temp_path, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        
        whitelist_service.save_entries(entries)
        
        temp_path.unlink()
        
        stats = whitelist_service.get_whitelist_stats()
        
        return {
            "message": "Whitelist uploaded and reloaded successfully",
            "stats": stats
        }
        
    except json.JSONDecodeError:
        if temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

@router.post("/generate/")
async def generate_whitelist(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are accepted")
    
    temp_path = None
    try:
        temp_path = Path(f"temp_{file.filename}")
        content = await file.read()
        
        with open(temp_path, "wb") as f:
            f.write(content)
        
        entries = whitelist_service.generate(temp_path)
        
        temp_path.unlink()
        
        stats = whitelist_service.get_whitelist_stats()
        
        return {
            "message": "Whitelist generated successfully from Excel file",
            "entries_generated": len(entries),
            "stats": stats
        }
        
    except Exception as e:
        if temp_path and temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

@router.get("/stats/")    
def get_whitelist_stats() -> Dict[str, Any]:
    try:
        stats = whitelist_service.get_whitelist_stats()
        return {
            "message": "Whitelist statistics retrieved successfully",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")
    
@router.get("/entries/", response_model = List[WhitelistEntry])
def get_all_entries() -> List[WhitelistEntry]:
    try:
        return whitelist_service.get_entries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {str(e)}")
