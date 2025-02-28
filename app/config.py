from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str = "abc123"
    algorithm: str = "HS256"
    token_expire_min: int = 30
    sqlite_file_name: str = "database.db"
    sqlite_url: str = f"sqlite:///{sqlite_file_name}"
    openai_api_key: str = "abc123"

    model_config = SettingsConfigDict(env_file=".env.development.local")
