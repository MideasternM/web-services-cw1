from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.recipe import Recipe
from app.routers import recipes

app = FastAPI(title="Nutrition and Recipe Analytics API")
Base.metadata.create_all(bind=engine)
app.include_router(recipes.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
