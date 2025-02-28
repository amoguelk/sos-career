from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str = "abc"
    algorithm: str = "HS256"
    token_expire_min: int = 30
    sqlite_file_name: str = "database.db"
    sqlite_url: str = f"sqlite:///{sqlite_file_name}"

    model_config = SettingsConfigDict(env_file=".env.development.local")
