from fastapi import APIRouter, Depends, HTTPException
from app.schemas import DownloadRequest
from app.crud import create_download
from app.auth import verify_token
from app.messaging.rabbitmq_publisher import publish_download_message

AUDIO_FORMATS = ['mp3', 'm4a', 'aac', 'wav', 'opus']
VIDEO_FORMATS = ['mp4', 'webm', 'mkv']

router = APIRouter()

@router.post("/download")
async def download_media(request: DownloadRequest, token: dict = Depends(verify_token)):
    format_requested = request.format.lower()

    if format_requested not in AUDIO_FORMATS + VIDEO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato inválido. Escolha entre: {AUDIO_FORMATS + VIDEO_FORMATS}"
        )

    download_id = await create_download(
        user_id=token.get("sub"),
        video_url=request.url,
        format=format_requested,
    )

    message = {
        "id": download_id,
        "url": request.url,
        "format": format_requested,
        "user_id": token.get("sub")
    }

    try:
        await publish_download_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enfileirar download: {str(e)}")
    
    return {
        "message": "Download enfileirado com sucesso.",
        "file_id": download_id,
        "status": "pending"
    }