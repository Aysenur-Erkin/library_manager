from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./library.db"
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "http://127.0.0.1:8000,http://localhost:8000"
    ENV: str = "development"
    @property
    def cors_origins_list(self): return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]
    class Config: env_file = ".env"
settings = Settings()
