from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    SECRET_KEY: str = "super-secret"

    class Config:
        env_file = ".env"

settings = Settings()
