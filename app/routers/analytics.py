from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.recipes import get_category_counts


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/recipes/by-category")
def recipe_counts_by_category(db: Session = Depends(get_db)) -> dict[str, list[dict[str, int | str]]]:
    return {"categories": get_category_counts(db)}
