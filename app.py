from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import uuid
import os

app = FastAPI()

# Diretório onde os downloads serão salvos
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Formatos permitidos
AUDIO_FORMATS = ['mp3', 'm4a', 'aac', 'wav', 'opus']
VIDEO_FORMATS = ['mp4', 'webm', 'mkv']

class DownloadRequest(BaseModel):
    url: str
    format: str  # Exemplo: 'mp3' ou 'mp4'

@app.post("/download")
async def download_media(request: DownloadRequest):
    format_requested = request.format.lower()

    if format_requested not in AUDIO_FORMATS + VIDEO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato inválido. Escolha entre: {AUDIO_FORMATS + VIDEO_FORMATS}"
        )

    # Nome de arquivo aleatório para evitar conflito
    random_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{random_id}.%(ext)s")

    ydl_opts = {}

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
    else:  # formato de vídeo
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': format_requested,
            'outtmpl': output_template,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])

        # Pega o primeiro arquivo que foi gerado
        downloaded_files = os.listdir(DOWNLOAD_DIR)
        matching_files = [f for f in downloaded_files if random_id in f]

        if not matching_files:
            raise HTTPException(status_code=500, detail="Erro ao baixar o arquivo.")

        file_name = matching_files[0]

        return {
            "message": "Download concluído com sucesso.",
            "file_name": file_name,
            "download_link": f"/files/{file_name}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.responses import FileResponse

@app.get("/files/{file_name}")
async def get_file(file_name: str):
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name)
    else:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
