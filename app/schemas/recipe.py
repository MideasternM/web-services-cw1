from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = ""
    category: str = Field(min_length=1, max_length=50)
    difficulty: str = Field(pattern="^(easy|medium|hard)$")
    servings: int = Field(gt=0)
    instructions: str = ""


class RecipeSummary(BaseModel):
    id: int
    name: str
    description: str
    category: str
    difficulty: str
    servings: int
    instructions: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecipeListResponse(BaseModel):
    items: list[RecipeSummary]
