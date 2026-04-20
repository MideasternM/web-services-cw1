from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.recipe import Recipe


def get_category_counts(db: Session) -> list[dict[str, int | str]]:
    rows = db.query(Recipe.category, func.count(Recipe.id)).group_by(Recipe.category).all()
    return [{"category": category, "recipe_count": count} for category, count in rows]
