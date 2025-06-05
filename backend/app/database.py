from sqlalchemy import create_engine
from databases import Database
from app.models import Base
from app.core.settings import settings

DATABASE_URL = settings.DATABASE_URL

# Engine síncrono para criar tabelas
engine = create_engine(DATABASE_URL.replace('asyncpg', 'psycopg2'))

# Database assíncrono para FastAPI
database = Database(DATABASE_URL)

def create_tables():
    Base.metadata.create_all(bind=engine)
