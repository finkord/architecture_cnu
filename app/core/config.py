from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Payment Service"
    VERSION: str = "1.0.0"
    DATABASE_URL: str
    RABBITMQ_URL: str
    STRIPE_API_KEY: str = "sk_test_mock"
    API_TIMEOUT: int = 5

    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_name: Optional[str] = None
    rmq_user: Optional[str] = None
    rmq_password: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
