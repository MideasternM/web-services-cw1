from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import analytics
from app.routers import ingredients
from app.routers import recipes
from app.models import ingredient, recipe, recipe_ingredient

app = FastAPI(title="Nutrition and Recipe Analytics API")
Base.metadata.create_all(bind=engine)
app.include_router(recipes.router)
app.include_router(ingredients.router)
app.include_router(analytics.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
