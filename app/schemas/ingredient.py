from pydantic import BaseModel, ConfigDict, Field


class IngredientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    calories_per_100g: float = Field(ge=0)
    protein_per_100g: float = Field(ge=0)
    fat_per_100g: float = Field(ge=0)
    carbs_per_100g: float = Field(ge=0)
    contains_allergen: bool = False
    allergen_notes: str = ""


class IngredientSummary(IngredientCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class IngredientListResponse(BaseModel):
    items: list[IngredientSummary]
