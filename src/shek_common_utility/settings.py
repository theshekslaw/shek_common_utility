from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False,
    )

    service_name: str = Field(default="unnamed-service")
    log_level: str = Field(default="INFO")
    log_json: bool = Field(default=True)

    auth_token: str = Field(default="", description="Bearer token expected on requests.")
