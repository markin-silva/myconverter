from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import database, create_tables
from app.routes import download, files

app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost:3000",  # Frontend Vue.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    create_tables()
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Incluir rotas
app.include_router(download.router)
app.include_router(files.router)