"""Environment configuration.

python-dotenv is used for local development when a `.env` file is present.
Missing variables fall back to empty strings or the local database URL.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/clinical_cases"
    openai_api_key: str = ""
    openai_model: str = "gpt-5"
    loinc_username: str = ""
    loinc_password: str = ""
    snomed_base_url: str = ""
    snomed_api_token: str = ""
    mimic_local_path: str = ""


def get_settings() -> Settings:
    return Settings()
