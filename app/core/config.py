import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Nutrition and Recipe Analytics API")
    api_key: str = os.getenv("API_KEY", "dev-secret-key")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./nutrition.db")


settings = Settings()
