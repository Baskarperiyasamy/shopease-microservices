from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ShopEase Product Service"
    app_version: str = "1.0.0"
    debug: bool = False
    default_page_limit: int = 10
    max_page_limit: int = 100

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
