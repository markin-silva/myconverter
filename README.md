# 🎬 FastAPI + Vue.js YouTube Downloader

[Uma aplicação completa para baixar vídeos ou áudios do YouTube via link com autenticação Keycloak!](https://github.com/markin-silva/myconverter)

---

## 🚀 Tecnologias usadas
- [FastAPI](https://fastapi.tiangolo.com/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Uvicorn](https://www.uvicorn.org/)
- [FFmpeg](https://ffmpeg.org/) (para conversão de áudio e vídeo)
- [Keycloak](https://www.keycloak.org/) (para autenticação)
- [Vue.js 3](https://vuejs.org/) (para frontend)
- [axios](https://axios-http.com/) (requisições HTTP no front)

---

## ⚙️ Setup Local

### Pré-requisitos
- Docker
- Docker Compose
- Python 3.10+
- FFmpeg (para conversão de áudio e vídeo)

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

## 📦 Estrutura do projeto

```
myconverter/
├── backend/        # Código FastAPI + yt-dlp
├── frontend/       # Código Vue.js + Keycloak-js
├── keycloak/       # Realm export JSON para configuração automática
├── docker-compose.yml
├── README.md
```

---

## 🔐 Autenticação Keycloak

O ambiente já sobe com:

- Realm: `myrealm`
- Client: `myconverter`
- Usuário: `user`
- Senha: `password`

Não é necessário nenhuma configuração manual! Tudo é importado automaticamente via `realm-export.json`.

---

## 📥 Como usar

### 1. Frontend

- Acesse o Frontend no navegador:

```
http://localhost:3000
```

- Faça login com:
  - **Usuário**: `user`
  - **Senha**: `password`

- Após login:
  - Insira a URL do vídeo do YouTube.
  - Escolha o formato (`mp3` ou `mp4`).
  - Clique em **Baixar**.
  - O download será iniciado automaticamente.

**Importante**: Todas as requisições enviam o `Bearer Token` obtido via Keycloak.

---

### 2. Endpoints disponíveis (Backend)

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

Baixa o arquivo gerado.

**Requer Bearer Token no Header**:

```http
Authorization: Bearer <token>
```

---

## 📝 Observações
- Todos os arquivos baixados ficam salvos na pasta `downloads/` do container backend.
- A conversão para `.mp3` e `.mp4` exige o `ffmpeg` — já incluímos isso na imagem Docker.
- Esta aplicação é para fins educacionais. Respeite os [Termos de Serviço do YouTube](https://www.youtube.com/t/terms).
- Os downloads e tokens são válidos apenas em ambiente de desenvolvimento.
- O frontend Vue.js integra automaticamente com o Keycloak para login e consumo dos endpoints protegidos.
