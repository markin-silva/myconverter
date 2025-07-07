from fastapi import APIRouter, Depends, HTTPException
from app.auth import verify_token
from app.storage.s3 import generate_presigned_url
from app.crud import get_download_by_file_name

router = APIRouter()

@router.get("/files/{file_name}")
async def get_file(file_name: str, token: dict = Depends(verify_token)):
    download = await get_download_by_file_name(file_name)

    if not download or not download.s3_key:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

    presigned_url = generate_presigned_url(download.s3_key)
    return {"url": presigned_url}
