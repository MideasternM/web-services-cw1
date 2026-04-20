from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Nutrition and Recipe Analytics API"
    api_key: str = "dev-secret-key"
    database_url: str = "sqlite:///./nutrition.db"


settings = Settings()
