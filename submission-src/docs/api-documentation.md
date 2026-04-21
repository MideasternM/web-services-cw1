# Nutrition and Recipe Analytics API Documentation

## Overview

Base URL for local development:

```text
http://127.0.0.1:8000
```

Interactive OpenAPI docs:

```text
http://127.0.0.1:8000/docs
```

All responses are JSON.

## Authentication

Protected write endpoints require an API key in the request header:

```http
X-API-Key: dev-secret-key
```

If the key is missing or invalid, the API returns:

```json
{
  "detail": {
    "error": "UNAUTHORIZED",
    "message": "Invalid or missing API key"
  }
}
```

## Health

### `GET /health`

Checks whether the API is running.

Response:

```json
{
  "status": "ok"
}
```

## Recipes

### `GET /recipes`

Returns all recipes.

Response:

```json
{
  "items": [
    {
      "id": 1,
      "name": "Breakfast Bowl",
      "description": "Yogurt, banana, and oats",
      "category": "breakfast",
      "difficulty": "easy",
      "servings": 2,
      "instructions": "Combine all ingredients.",
      "created_at": "2026-04-20T06:00:00Z",
      "updated_at": "2026-04-20T06:00:00Z"
    }
  ]
}
```

### `GET /recipes/search`

Filters recipes by query parameters.

Supported query parameters:

- `category`
- `difficulty`
- `max_servings`

Example:

```http
GET /recipes/search?category=breakfast&difficulty=easy
```

### `GET /recipes/{recipe_id}`

Returns a single recipe.

Not found response:

```json
{
  "detail": {
    "error": "RESOURCE_NOT_FOUND",
    "message": "Recipe with id 99 was not found"
  }
}
```

### `POST /recipes`

Creates a recipe. Protected by API key.

Request body:

```json
{
  "name": "Berry Oats",
  "description": "Oats with berries",
  "category": "breakfast",
  "difficulty": "easy",
  "servings": 1,
  "instructions": "Mix and serve"
}
```

Successful response status: `201 Created`

### `PUT /recipes/{recipe_id}`

Updates a recipe. Protected by API key.

Uses the same request body shape as `POST /recipes`.

Successful response status: `200 OK`

### `DELETE /recipes/{recipe_id}`

Deletes a recipe. Protected by API key.

Successful response status: `204 No Content`

## Ingredients

### `GET /ingredients`

Returns all ingredients.

### `GET /ingredients/{ingredient_id}`

Returns a single ingredient.

### `POST /ingredients`

Creates an ingredient. Protected by API key.

Request body:

```json
{
  "name": "Greek Yogurt",
  "calories_per_100g": 65,
  "protein_per_100g": 11,
  "fat_per_100g": 0.5,
  "carbs_per_100g": 4.0,
  "contains_allergen": true,
  "allergen_notes": "milk"
}
```

Validation errors return `422 Unprocessable Entity`.

### `PUT /ingredients/{ingredient_id}`

Updates an ingredient. Protected by API key.

### `DELETE /ingredients/{ingredient_id}`

Deletes an ingredient. Protected by API key.

## Recipe Ingredient Links

### `POST /recipes/{recipe_id}/ingredients`

Links an ingredient to a recipe with a quantity. Protected by API key.

Request body:

```json
{
  "ingredient_id": 2,
  "quantity_g": 100
}
```

Successful response:

```json
{
  "status": "linked"
}
```

### `DELETE /recipes/{recipe_id}/ingredients/{ingredient_id}`

Removes an ingredient from a recipe. Protected by API key.

Successful response status: `204 No Content`

If the link does not exist:

```json
{
  "detail": {
    "error": "RESOURCE_NOT_FOUND",
    "message": "Ingredient 2 was not linked to recipe 1"
  }
}
```

## Analytics

### `GET /recipes/{recipe_id}/nutrition`

Calculates total and per-serving nutrition for a recipe.

Response:

```json
{
  "recipe_id": 1,
  "recipe_name": "Banana Yogurt Bowl",
  "servings": 2,
  "total": {
    "calories": 209.0,
    "protein": 21.1,
    "fat": 4.3,
    "carbs": 30.8
  },
  "per_serving": {
    "calories": 104.5,
    "protein": 10.55,
    "fat": 2.15,
    "carbs": 15.4
  }
}
```

### `GET /analytics/recipes/by-category`

Returns recipe counts grouped by category.

Response:

```json
{
  "categories": [
    {
      "category": "breakfast",
      "recipe_count": 3
    },
    {
      "category": "lunch",
      "recipe_count": 1
    }
  ]
}
```

## Status Codes

- `200 OK`: successful read or update
- `201 Created`: successful create
- `204 No Content`: successful delete
- `401 Unauthorized`: missing or invalid API key
- `404 Not Found`: resource or relationship not found
- `422 Unprocessable Entity`: validation failure

## Running the API

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```
