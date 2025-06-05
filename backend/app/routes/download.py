from fastapi import APIRouter, Depends, HTTPException
import os
import uuid
import yt_dlp
from app.schemas import DownloadRequest
from app.crud import create_download, update_download_status
from app.database import database
from app.models import DownloadStatus
from app.auth import verify_token  # função de verificação de token que você já tem

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

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

    random_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{random_id}.%(ext)s")

    await create_download(
        user_id=token.get("sub"),
        video_url=request.url,
        format=format_requested,
        file_path=random_id
    )

    if format_requested in AUDIO_FORMATS:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_requested,
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
        }
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': format_requested,
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegMerger'
            }],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])

        downloaded_files = os.listdir(DOWNLOAD_DIR)
        matching_files = [f for f in downloaded_files if random_id in f]

        if not matching_files:
            raise HTTPException(status_code=500, detail="Erro ao baixar o arquivo.")

        file_name = matching_files[0]

        await update_download_status(random_id, DownloadStatus.completed.name)

        return {
            "message": "Download concluído com sucesso.",
            "file_name": file_name,
            "download_link": f"/files/{file_name}"
        }

    except Exception as e:
        await update_download_status(random_id, DownloadStatus.failed.name)
        raise HTTPException(status_code=500, detail=str(e))
