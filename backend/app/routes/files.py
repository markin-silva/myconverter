from fastapi import APIRouter, Depends, HTTPException
import os
from fastapi.responses import FileResponse
from app.auth import verify_token

DOWNLOAD_DIR = "/app/downloads"

router = APIRouter()

@router.get("/files/{file_name}")
async def get_file(file_name: str, token: dict = Depends(verify_token)):
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name, media_type='application/octet-stream')
    else:
        raise HTTPException(status_code=404, detail=f"Arquivo {file_name} não encontrado.")
