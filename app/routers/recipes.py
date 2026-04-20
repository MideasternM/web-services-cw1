from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_api_key
from app.db.database import get_db
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeListResponse, RecipeSummary


router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=RecipeListResponse)
def list_recipes(db: Session = Depends(get_db)) -> RecipeListResponse:
    return RecipeListResponse(items=db.query(Recipe).all())


@router.get("/{recipe_id}", response_model=RecipeSummary)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> RecipeSummary:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Recipe with id {recipe_id} was not found"},
        )
    return recipe


@router.post("", response_model=RecipeSummary, status_code=201, dependencies=[Depends(verify_api_key)])
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)) -> RecipeSummary:
    recipe = Recipe(**payload.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe
