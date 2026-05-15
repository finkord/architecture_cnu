from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Payment Microservice"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # PostgreSQL settings
    # Defaulting to an async in-memory SQLite for immediate runnable demo, but can be configured
    # For actual PostgreSQL: postgresql+asyncpg://user:password@host:port/db
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
