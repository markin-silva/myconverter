# 🎬 FastAPI YouTube Downloader

Uma API simples para baixar vídeos ou áudios do YouTube via link!

---

## 🚀 Tecnologias usadas
- [FastAPI](https://fastapi.tiangolo.com/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Uvicorn](https://www.uvicorn.org/)
- [FFmpeg](https://ffmpeg.org/) (para conversão de áudio)

---

## ⚙️ Setup Local

### Pré-requisitos
- Docker
- Docker Compose

### Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/fastapi-downloader.git
cd fastapi-downloader
```

2. Construa e suba os containers:

```bash
docker compose up --build
```

3. Acesse a documentação automática:

```bash
http://localhost:8000/docs
```