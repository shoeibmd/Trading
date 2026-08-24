from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Financial Terminal API"
    environment: str = "development"
    postgres_dsn: str | None = None
    redis_url: str | None = None

    class Config:
        env_file = ".env"
        env_prefix = "APP_"

settings = Settings()
