from pydantic import BaseModel, Field


class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    quantity_g: float = Field(gt=0)


class NutritionTotals(BaseModel):
    calories: float
    protein: float
    fat: float
    carbs: float


class RecipeNutritionResponse(BaseModel):
    recipe_id: int
    recipe_name: str
    servings: int
    total: NutritionTotals
    per_serving: NutritionTotals
