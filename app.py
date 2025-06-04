import os
import time
import requests

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from pydantic import BaseModel
import yt_dlp
import uuid
from fastapi.responses import FileResponse

# Diretório onde os downloads serão salvos
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configuração de Keycloak
KEYCLOAK_URL = "http://keycloak:8080/realms/myrealm"
OPENID_CONFIG_URL = f"{KEYCLOAK_URL}/.well-known/openid-configuration"

def wait_for_keycloak():
    print("🔄 Aguardando o Keycloak estar pronto...")
    while True:
        try:
            response = requests.get(OPENID_CONFIG_URL)
            if response.status_code == 200:
                print("✅ Keycloak está pronto!")
                break
        except Exception as e:
            print(f"⏳ Keycloak ainda não respondeu... ({e})")
        time.sleep(3)

# Aguarda o Keycloak ficar disponível
wait_for_keycloak()

# Pega as configurações do OpenID depois que o Keycloak está pronto
OPENID = requests.get(OPENID_CONFIG_URL).json()
PUBLIC_KEY = requests.get(OPENID["jwks_uri"]).json()["keys"][0]
ALGORITHMS = ["RS256"]

app = FastAPI()

AUDIO_FORMATS = ['mp3', 'm4a', 'aac', 'wav', 'opus']
VIDEO_FORMATS = ['mp4', 'webm', 'mkv']

# OAuth2 via Keycloak
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_URL}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_URL}/protocol/openid-connect/token"
)

# Função para verificar o token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            jwt.algorithms.RSAAlgorithm.from_jwk(PUBLIC_KEY),
            algorithms=ALGORITHMS,
            audience="account",  # ou ajuste para o client_id correto se necessário
            issuer=f"{KEYCLOAK_URL}"
        )
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Modelo para o corpo da requisição
class DownloadRequest(BaseModel):
    url: str
    format: str  # Exemplo: 'mp3' ou 'mp4'

# Endpoint para baixar mídia
@app.post("/download")
async def download_media(request: DownloadRequest, token: dict = Depends(verify_token)):
    format_requested = request.format.lower()

    if format_requested not in AUDIO_FORMATS + VIDEO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato inválido. Escolha entre: {AUDIO_FORMATS + VIDEO_FORMATS}"
        )

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
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': format_requested,
            'outtmpl': output_template,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])

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

# Endpoint para servir arquivos
@app.get("/files/{file_name}")
async def get_file(file_name: str, token: dict = Depends(verify_token)):
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name)
    else:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
