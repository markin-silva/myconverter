# 🎬 FastAPI YouTube Downloader

[Uma API simples para baixar vídeos ou áudios do YouTube via link!](https://github.com/markin-silva/myconverter)

---

## 🚀 Tecnologias usadas
- [FastAPI](https://fastapi.tiangolo.com/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Uvicorn](https://www.uvicorn.org/)
- [FFmpeg](https://ffmpeg.org/) (para conversão de áudio)
- [Keycloak](https://www.keycloak.org/) (para autenticação)

---

## ⚙️ Setup Local

### Pré-requisitos
- Docker
- Docker Compose
- Python 3.10+
- FFmpeg (para conversão de áudio)

---

### 🐳 Como rodar o projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/markin-silva/myconverter
cd myconverter
```

2. **Construa e suba os containers:**

```bash
docker compose up --build
```

---

## 🔐 Autenticação Keycloak

O ambiente já sobe com:

- Realm: `myrealm`
- Client: `fastapi-client`
- Usuário: `user`
- Senha: `password`

Não é necessário nenhuma configuração manual! Tudo é importado automaticamente.

---

## 📥 Como usar

### 1. Autenticação

- Faça login no Keycloak no Client `fastapi-client`.
- Pegue o **Access Token** (JWT) após o login.
- Nos requests da API, envie o token no cabeçalho:

```http
Authorization: Bearer <seu_access_token>
```

---

### 2. Endpoints disponíveis

#### `POST /download`

Baixa o vídeo ou áudio do YouTube no formato desejado.

**Requer Bearer Token no Header**:

```http
Authorization: Bearer <token>
```

**Body JSON**:

```json
{
  "url": "https://www.youtube.com/watch?v=exemplo",
  "format": "mp3"
}
```

**Formatos suportados**:
- Áudio: `mp3`, `m4a`, `aac`, `wav`, `opus`
- Vídeo: `mp4`, `webm`, `mkv`

**Resposta**:

```json
{
  "message": "Download concluído com sucesso.",
  "file_name": "arquivo-gerado.mp3",
  "download_link": "/files/arquivo-gerado.mp3"
}
```

---

#### `GET /files/{file_name}`

Baixa o arquivo que foi gerado.

**Requer Bearer Token no Header**:

```http
Authorization: Bearer <token>
```

---

## 📝 Observações
- Todos os arquivos baixados ficam salvos na pasta `downloads/`.
- A conversão para `.mp3` exige que o `ffmpeg` esteja disponível — já incluímos isso na imagem Docker.
- Esta API é para fins educacionais. Respeite os [Termos de Serviço do YouTube](https://www.youtube.com/t/terms).
- Os downloads e tokens são válidos apenas em ambiente de desenvolvimento.
