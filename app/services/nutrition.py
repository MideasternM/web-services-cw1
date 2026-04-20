from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.nutrition import NutritionTotals, RecipeNutritionResponse


def build_recipe_nutrition(recipe: Recipe, db: Session) -> RecipeNutritionResponse:
    links = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe.id).all()
    total_calories = 0.0
    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0

    for link in links:
        ingredient = db.query(Ingredient).filter(Ingredient.id == link.ingredient_id).first()
        scale = link.quantity_g / 100
        total_calories += ingredient.calories_per_100g * scale
        total_protein += ingredient.protein_per_100g * scale
        total_fat += ingredient.fat_per_100g * scale
        total_carbs += ingredient.carbs_per_100g * scale

    total = NutritionTotals(
        calories=round(total_calories, 2),
        protein=round(total_protein, 2),
        fat=round(total_fat, 2),
        carbs=round(total_carbs, 2),
    )
    per_serving = NutritionTotals(
        calories=round(total.calories / recipe.servings, 2),
        protein=round(total.protein / recipe.servings, 2),
        fat=round(total.fat / recipe.servings, 2),
        carbs=round(total.carbs / recipe.servings, 2),
    )
    return RecipeNutritionResponse(
        recipe_id=recipe.id,
        recipe_name=recipe.name,
        servings=recipe.servings,
        total=total,
        per_serving=per_serving,
    )
