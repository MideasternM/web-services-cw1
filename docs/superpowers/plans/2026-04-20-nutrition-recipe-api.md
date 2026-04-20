# Nutrition and Recipe Analytics API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a FastAPI and SQLite nutrition API with CRUD, analytics, API-key-protected write operations, tests, seed data, and coursework-ready project structure.

**Architecture:** The project uses a layered FastAPI structure with SQLAlchemy models, Pydantic schemas, dedicated routers, and service modules for nutrition calculations and query logic. SQLite keeps the runtime local and reliable for the oral exam, while generated OpenAPI docs provide a base for the required API documentation deliverable.

**Tech Stack:** Python 3.13, FastAPI, SQLAlchemy, Pydantic, pytest, SQLite, uvicorn

---

### Task 1: Scaffold Project Structure and Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `app/main.py`
- Create: `app/core/config.py`
- Create: `app/db/database.py`
- Create: `app/tests/test_health.py`
- Modify: `.gitignore`

- [x] **Step 1: Write the failing health test**

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_health.py -v`
Expected: FAIL because `app.main` or `/health` does not exist yet.

- [x] **Step 3: Write minimal implementation**

```python
from fastapi import FastAPI


app = FastAPI(title="Nutrition and Recipe Analytics API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

```python
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Nutrition and Recipe Analytics API"
    api_key: str = "dev-secret-key"
    database_url: str = "sqlite:///./nutrition.db"


settings = Settings()
```

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

```text
fastapi
uvicorn
sqlalchemy
pydantic
pytest
httpx
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_health.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add requirements.txt app/main.py app/core/config.py app/db/database.py app/tests/test_health.py .gitignore
git commit -m "feat: scaffold fastapi app with health endpoint"
```

### Task 2: Add Recipe Data Model and CRUD Read Flow

**Files:**
- Create: `app/models/recipe.py`
- Create: `app/schemas/recipe.py`
- Create: `app/routers/recipes.py`
- Create: `app/tests/test_recipes.py`
- Modify: `app/main.py`
- Modify: `app/db/database.py`

- [x] **Step 1: Write the failing recipe list and detail tests**

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_empty_recipe_list_returns_empty_items():
    response = client.get("/recipes")

    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_missing_recipe_returns_404():
    response = client.get("/recipes/999")

    assert response.status_code == 404
    assert response.json()["detail"]["error"] == "RESOURCE_NOT_FOUND"
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_recipes.py -v`
Expected: FAIL because recipe routes and model are missing.

- [x] **Step 3: Write minimal implementation**

```python
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    servings: Mapped[int] = mapped_column(Integer, nullable=False)
    instructions: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

```python
from datetime import datetime

from pydantic import BaseModel


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

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    items: list[RecipeSummary]
```

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeListResponse, RecipeSummary


router = APIRouter(prefix="/recipes", tags=["recipes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
```

```python
from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import recipes


app = FastAPI(title="Nutrition and Recipe Analytics API")
Base.metadata.create_all(bind=engine)
app.include_router(recipes.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_recipes.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add app/models/recipe.py app/schemas/recipe.py app/routers/recipes.py app/tests/test_recipes.py app/main.py app/db/database.py
git commit -m "feat: add recipe read endpoints"
```

### Task 3: Add API Key Auth and Recipe Write Endpoints

**Files:**
- Create: `app/core/security.py`
- Modify: `app/schemas/recipe.py`
- Modify: `app/routers/recipes.py`
- Modify: `app/tests/test_recipes.py`

- [x] **Step 1: Write the failing auth and create recipe tests**

```python
def test_create_recipe_requires_api_key():
    payload = {
        "name": "Berry Oats",
        "description": "Oats with berries",
        "category": "breakfast",
        "difficulty": "easy",
        "servings": 1,
        "instructions": "Mix and serve",
    }

    response = client.post("/recipes", json=payload)

    assert response.status_code == 401


def test_create_recipe_with_api_key_returns_created():
    payload = {
        "name": "Berry Oats",
        "description": "Oats with berries",
        "category": "breakfast",
        "difficulty": "easy",
        "servings": 1,
        "instructions": "Mix and serve",
    }

    response = client.post("/recipes", json=payload, headers={"X-API-Key": "dev-secret-key"})

    assert response.status_code == 201
    assert response.json()["name"] == "Berry Oats"
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_recipes.py -v`
Expected: FAIL because auth and create route are missing.

- [x] **Step 3: Write minimal implementation**

```python
from fastapi import Header, HTTPException

from app.core.config import settings


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail={"error": "UNAUTHORIZED", "message": "Invalid or missing API key"},
        )
```

```python
from pydantic import BaseModel, Field


class RecipeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = ""
    category: str = Field(min_length=1, max_length=50)
    difficulty: str = Field(pattern="^(easy|medium|hard)$")
    servings: int = Field(gt=0)
    instructions: str = ""
```

```python
@router.post("", response_model=RecipeSummary, status_code=201, dependencies=[Depends(verify_api_key)])
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)) -> RecipeSummary:
    recipe = Recipe(**payload.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_recipes.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add app/core/security.py app/schemas/recipe.py app/routers/recipes.py app/tests/test_recipes.py
git commit -m "feat: protect recipe writes with api key auth"
```

### Task 4: Complete Recipe Update and Delete

**Files:**
- Modify: `app/routers/recipes.py`
- Modify: `app/tests/test_recipes.py`

- [x] **Step 1: Write the failing update and delete tests**

```python
def test_update_recipe_changes_fields():
    created = client.post(
        "/recipes",
        json={
            "name": "Berry Oats",
            "description": "Oats with berries",
            "category": "breakfast",
            "difficulty": "easy",
            "servings": 1,
            "instructions": "Mix and serve",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )

    recipe_id = created.json()["id"]
    response = client.put(
        f"/recipes/{recipe_id}",
        json={
            "name": "Berry Oats Deluxe",
            "description": "Oats with berries and nuts",
            "category": "breakfast",
            "difficulty": "medium",
            "servings": 2,
            "instructions": "Mix and serve chilled",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Berry Oats Deluxe"


def test_delete_recipe_returns_204_and_resource_disappears():
    created = client.post(
        "/recipes",
        json={
            "name": "Tomato Soup",
            "description": "Light soup",
            "category": "lunch",
            "difficulty": "easy",
            "servings": 2,
            "instructions": "Blend and boil",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )
    recipe_id = created.json()["id"]

    delete_response = client.delete(f"/recipes/{recipe_id}", headers={"X-API-Key": "dev-secret-key"})
    assert delete_response.status_code == 204

    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_recipes.py -v`
Expected: FAIL because update and delete routes are missing.

- [x] **Step 3: Write minimal implementation**

```python
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
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_recipes.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add app/routers/recipes.py app/tests/test_recipes.py
git commit -m "feat: complete recipe update and delete operations"
```

### Task 5: Add Ingredient Model and CRUD

**Files:**
- Create: `app/models/ingredient.py`
- Create: `app/schemas/ingredient.py`
- Create: `app/routers/ingredients.py`
- Create: `app/tests/test_ingredients.py`
- Modify: `app/main.py`

- [x] **Step 1: Write the failing ingredient tests**

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_empty_ingredient_list_returns_empty_items():
    response = client.get("/ingredients")

    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_create_ingredient_rejects_negative_nutrition():
    response = client.post(
        "/ingredients",
        json={
            "name": "Yogurt",
            "calories_per_100g": -1,
            "protein_per_100g": 10,
            "fat_per_100g": 4,
            "carbs_per_100g": 7,
            "contains_allergen": True,
            "allergen_notes": "milk",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )

    assert response.status_code == 422
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_ingredients.py -v`
Expected: FAIL because ingredient routes and model are missing.

- [x] **Step 3: Write minimal implementation**

```python
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    calories_per_100g: Mapped[float] = mapped_column(Float, nullable=False)
    protein_per_100g: Mapped[float] = mapped_column(Float, nullable=False)
    fat_per_100g: Mapped[float] = mapped_column(Float, nullable=False)
    carbs_per_100g: Mapped[float] = mapped_column(Float, nullable=False)
    contains_allergen: Mapped[bool] = mapped_column(Boolean, default=False)
    allergen_notes: Mapped[str] = mapped_column(String(255), default="")
```

```python
from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True


class IngredientListResponse(BaseModel):
    items: list[IngredientSummary]
```

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_api_key
from app.db.database import SessionLocal
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientListResponse, IngredientSummary


router = APIRouter(prefix="/ingredients", tags=["ingredients"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_ingredients.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add app/models/ingredient.py app/schemas/ingredient.py app/routers/ingredients.py app/tests/test_ingredients.py app/main.py
git commit -m "feat: add ingredient model and create endpoint"
```

### Task 6: Complete Ingredient Update and Delete

**Files:**
- Modify: `app/routers/ingredients.py`
- Modify: `app/tests/test_ingredients.py`

- [x] **Step 1: Write the failing ingredient update and delete tests**

```python
def test_update_ingredient_changes_values():
    created = client.post(
        "/ingredients",
        json={
            "name": "Yogurt",
            "calories_per_100g": 59,
            "protein_per_100g": 10,
            "fat_per_100g": 0.4,
            "carbs_per_100g": 3.6,
            "contains_allergen": True,
            "allergen_notes": "milk",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )
    ingredient_id = created.json()["id"]

    response = client.put(
        f"/ingredients/{ingredient_id}",
        json={
            "name": "Greek Yogurt",
            "calories_per_100g": 65,
            "protein_per_100g": 11,
            "fat_per_100g": 0.5,
            "carbs_per_100g": 4.0,
            "contains_allergen": True,
            "allergen_notes": "milk",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Greek Yogurt"


def test_delete_ingredient_returns_204():
    created = client.post(
        "/ingredients",
        json={
            "name": "Banana",
            "calories_per_100g": 89,
            "protein_per_100g": 1.1,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 22.8,
            "contains_allergen": False,
            "allergen_notes": "",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )
    ingredient_id = created.json()["id"]

    delete_response = client.delete(f"/ingredients/{ingredient_id}", headers={"X-API-Key": "dev-secret-key"})

    assert delete_response.status_code == 204
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_ingredients.py -v`
Expected: FAIL because ingredient update and delete routes are missing.

- [x] **Step 3: Write minimal implementation**

```python
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
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_ingredients.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add app/routers/ingredients.py app/tests/test_ingredients.py
git commit -m "feat: complete ingredient update and delete operations"
```

### Task 7: Add Recipe-Ingredient Linking and Nutrition Service

**Files:**
- Create: `app/models/recipe_ingredient.py`
- Create: `app/schemas/nutrition.py`
- Create: `app/services/nutrition.py`
- Modify: `app/routers/recipes.py`
- Modify: `app/tests/test_recipes.py`

- [x] **Step 1: Write the failing nutrition test**

```python
def test_recipe_nutrition_aggregates_ingredient_values():
    recipe_response = client.post(
        "/recipes",
        json={
            "name": "Banana Yogurt Bowl",
            "description": "Simple bowl",
            "category": "breakfast",
            "difficulty": "easy",
            "servings": 2,
            "instructions": "Mix ingredients",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )
    recipe_id = recipe_response.json()["id"]

    yogurt = client.post(
        "/ingredients",
        json={
            "name": "Yogurt",
            "calories_per_100g": 60,
            "protein_per_100g": 10,
            "fat_per_100g": 2,
            "carbs_per_100g": 4,
            "contains_allergen": True,
            "allergen_notes": "milk",
        },
        headers={"X-API-Key": "dev-secret-key"},
    ).json()

    banana = client.post(
        "/ingredients",
        json={
            "name": "Banana",
            "calories_per_100g": 89,
            "protein_per_100g": 1.1,
            "fat_per_100g": 0.3,
            "carbs_per_100g": 22.8,
            "contains_allergen": False,
            "allergen_notes": "",
        },
        headers={"X-API-Key": "dev-secret-key"},
    ).json()

    client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": yogurt["id"], "quantity_g": 200},
        headers={"X-API-Key": "dev-secret-key"},
    )
    client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": banana["id"], "quantity_g": 100},
        headers={"X-API-Key": "dev-secret-key"},
    )

    response = client.get(f"/recipes/{recipe_id}/nutrition")

    assert response.status_code == 200
    assert response.json()["total"]["calories"] == 209.0
    assert response.json()["per_serving"]["calories"] == 104.5
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_recipes.py -v`
Expected: FAIL because relationship model and nutrition endpoint are missing.

- [x] **Step 3: Write minimal implementation**

```python
from sqlalchemy import Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = (UniqueConstraint("recipe_id", "ingredient_id", name="uq_recipe_ingredient"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False)
    quantity_g: Mapped[float] = mapped_column(Float, nullable=False)
```

```python
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
```

```python
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
```

```python
@router.post("/{recipe_id}/ingredients", status_code=201, dependencies=[Depends(verify_api_key)])
def add_ingredient_to_recipe(recipe_id: int, payload: RecipeIngredientCreate, db: Session = Depends(get_db)) -> dict[str, str]:
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
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_recipes.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add app/models/recipe_ingredient.py app/schemas/nutrition.py app/services/nutrition.py app/routers/recipes.py app/tests/test_recipes.py
git commit -m "feat: add recipe nutrition analytics"
```

### Task 8: Add Search, Category Analytics, Seed Data, and README

**Files:**
- Create: `app/routers/analytics.py`
- Create: `app/services/recipes.py`
- Create: `app/db/seed.py`
- Create: `data/sample_ingredients.csv`
- Create: `data/sample_recipes.csv`
- Create: `README.md`
- Create: `app/tests/test_analytics.py`
- Modify: `app/main.py`

- [x] **Step 1: Write the failing analytics tests**

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_recipe_category_analytics_returns_counts():
    client.post(
        "/recipes",
        json={
            "name": "Smoothie",
            "description": "Fruit drink",
            "category": "breakfast",
            "difficulty": "easy",
            "servings": 1,
            "instructions": "Blend",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )
    client.post(
        "/recipes",
        json={
            "name": "Pasta Salad",
            "description": "Cold pasta",
            "category": "lunch",
            "difficulty": "easy",
            "servings": 2,
            "instructions": "Mix",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )

    response = client.get("/analytics/recipes/by-category")

    assert response.status_code == 200
    categories = {item["category"]: item["recipe_count"] for item in response.json()["categories"]}
    assert categories["breakfast"] >= 1
    assert categories["lunch"] >= 1
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest app/tests/test_analytics.py -v`
Expected: FAIL because analytics route is missing.

- [x] **Step 3: Write minimal implementation**

```python
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.recipe import Recipe


def get_category_counts(db: Session) -> list[dict[str, int | str]]:
    rows = db.query(Recipe.category, func.count(Recipe.id)).group_by(Recipe.category).all()
    return [{"category": category, "recipe_count": count} for category, count in rows]
```

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.recipes import get_category_counts


router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/recipes/by-category")
def recipe_counts_by_category(db: Session = Depends(get_db)) -> dict[str, list[dict[str, int | str]]]:
    return {"categories": get_category_counts(db)}
```

```python
# README content should include setup, run, test, API key, and docs location.
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest app/tests/test_analytics.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/routers/analytics.py app/services/recipes.py app/db/seed.py data/sample_ingredients.csv data/sample_recipes.csv README.md app/tests/test_analytics.py app/main.py
git commit -m "feat: add recipe analytics and project documentation"
```

### Task 9: Full Verification

**Files:**
- Modify: `docs/superpowers/plans/2026-04-20-nutrition-recipe-api.md`

- [x] **Step 1: Run the full test suite**

Run: `pytest app/tests -v`
Expected: PASS with all tests green.

- [x] **Step 2: Run a startup smoke check**

Run: `python -c "from app.main import app; print(app.title)"`
Expected: prints `Nutrition and Recipe Analytics API`

- [x] **Step 3: Update plan progress**

Mark completed tasks in this plan file.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/2026-04-20-nutrition-recipe-api.md
git commit -m "docs: record implementation progress"
```
