from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "CAMBIA_ESTO_POR_ALGO_SEGURO"  # cambia esto en producción o usa .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # 1 día

    DATABASE_URL: str = "sqlite:///./school.db"

    class Config:
        env_file = ".env"

settings = Settings()
