from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_api_key
from app.db.database import get_db
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientListResponse, IngredientSummary


router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("", response_model=IngredientListResponse)
def list_ingredients(db: Session = Depends(get_db)) -> IngredientListResponse:
    return IngredientListResponse(items=db.query(Ingredient).all())


@router.get("/{ingredient_id}", response_model=IngredientSummary)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)) -> IngredientSummary:
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Ingredient with id {ingredient_id} was not found"},
        )
    return ingredient


@router.post("", response_model=IngredientSummary, status_code=201, dependencies=[Depends(verify_api_key)])
def create_ingredient(payload: IngredientCreate, db: Session = Depends(get_db)) -> IngredientSummary:
    ingredient = Ingredient(**payload.model_dump())
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientSummary, dependencies=[Depends(verify_api_key)])
def update_ingredient(ingredient_id: int, payload: IngredientCreate, db: Session = Depends(get_db)) -> IngredientSummary:
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Ingredient with id {ingredient_id} was not found"},
        )

    for key, value in payload.model_dump().items():
        setattr(ingredient, key, value)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.delete("/{ingredient_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)) -> None:
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "RESOURCE_NOT_FOUND", "message": f"Ingredient with id {ingredient_id} was not found"},
        )

    db.delete(ingredient)
    db.commit()
