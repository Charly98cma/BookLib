from pydantic_settings import BaseSettings, SettingsConfigDict

class APISettings(BaseSettings):
    
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # PostgreSQL
    POSTGRES_HOST: str = "postgresql_db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "booklib_db_dev"
    POSTGRES_USER: str = "prod_user"
    POSTGRES_PASSWORD: str = "StrongPassword"

    # JWT parameters
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    SECRET_KEY: str

    # Load from environment on production
    model_config = SettingsConfigDict(env_file=".env")

settings = APISettings()