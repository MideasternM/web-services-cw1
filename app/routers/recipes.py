from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_api_key
from app.db.database import get_db
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.nutrition import RecipeIngredientCreate, RecipeNutritionResponse
from app.schemas.recipe import RecipeCreate, RecipeListResponse, RecipeSummary
from app.services.nutrition import build_recipe_nutrition


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


@router.get("/search", response_model=RecipeListResponse)
def search_recipes(
    category: str | None = None,
    difficulty: str | None = None,
    max_servings: int | None = None,
    db: Session = Depends(get_db),
) -> RecipeListResponse:
    query = db.query(Recipe)
    if category:
        query = query.filter(Recipe.category == category)
    if difficulty:
        query = query.filter(Recipe.difficulty == difficulty)
    if max_servings is not None:
        query = query.filter(Recipe.servings <= max_servings)
    return RecipeListResponse(items=query.all())


@router.post("", response_model=RecipeSummary, status_code=201, dependencies=[Depends(verify_api_key)])
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)) -> RecipeSummary:
    recipe = Recipe(**payload.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.put("/{recipe_id}", response_model=RecipeSummary, dependencies=[Depends(verify_api_key)])
def update_recipe(recipe_id: int, payload: RecipeCreate, db: Session = Depends(get_db)) -> RecipeSummary:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Recipe with id {recipe_id} was not found"},
        )

    for key, value in payload.model_dump().items():
        setattr(recipe, key, value)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)) -> None:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Recipe with id {recipe_id} was not found"},
        )

    db.delete(recipe)
    db.commit()


@router.post("/{recipe_id}/ingredients", status_code=201, dependencies=[Depends(verify_api_key)])
def add_ingredient_to_recipe(
    recipe_id: int, payload: RecipeIngredientCreate, db: Session = Depends(get_db)
) -> dict[str, str]:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    ingredient = db.query(Ingredient).filter(Ingredient.id == payload.ingredient_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Recipe with id {recipe_id} was not found"},
        )
    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Ingredient with id {payload.ingredient_id} was not found"},
        )

    link = RecipeIngredient(recipe_id=recipe_id, ingredient_id=payload.ingredient_id, quantity_g=payload.quantity_g)
    db.add(link)
    db.commit()
    return {"status": "linked"}


@router.get("/{recipe_id}/nutrition", response_model=RecipeNutritionResponse)
def get_recipe_nutrition(recipe_id: int, db: Session = Depends(get_db)) -> RecipeNutritionResponse:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Recipe with id {recipe_id} was not found"},
        )
    return build_recipe_nutrition(recipe, db)
