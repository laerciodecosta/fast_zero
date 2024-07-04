# fast_zero/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',  # é por conta do sistema operacional
    )

    DATABASE_URL: str
