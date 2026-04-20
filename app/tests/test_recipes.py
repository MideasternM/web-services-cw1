from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_empty_recipe_list_returns_empty_items() -> None:
    response = client.get("/recipes")

    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_missing_recipe_returns_404() -> None:
    response = client.get("/recipes/999")

    assert response.status_code == 404
    assert response.json()["detail"]["error"] == "RESOURCE_NOT_FOUND"


def test_create_recipe_requires_api_key() -> None:
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


def test_create_recipe_with_api_key_returns_created() -> None:
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


def test_update_recipe_changes_fields() -> None:
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


def test_delete_recipe_returns_204_and_resource_disappears() -> None:
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


def test_recipe_nutrition_aggregates_ingredient_values() -> None:
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

    link_yogurt = client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": yogurt["id"], "quantity_g": 200},
        headers={"X-API-Key": "dev-secret-key"},
    )
    link_banana = client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": banana["id"], "quantity_g": 100},
        headers={"X-API-Key": "dev-secret-key"},
    )

    assert link_yogurt.status_code == 201
    assert link_banana.status_code == 201

    response = client.get(f"/recipes/{recipe_id}/nutrition")

    assert response.status_code == 200
    assert response.json()["total"]["calories"] == 209.0
    assert response.json()["per_serving"]["calories"] == 104.5


def test_search_recipes_filters_by_category_and_difficulty() -> None:
    client.post(
        "/recipes",
        json={
            "name": "Quick Smoothie",
            "description": "Fruit smoothie",
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
            "name": "Roast Veg Tray",
            "description": "Roasted vegetables",
            "category": "dinner",
            "difficulty": "medium",
            "servings": 2,
            "instructions": "Roast",
        },
        headers={"X-API-Key": "dev-secret-key"},
    )

    response = client.get("/recipes/search", params={"category": "breakfast", "difficulty": "easy"})

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["name"] == "Quick Smoothie"


def test_remove_ingredient_from_recipe_updates_nutrition() -> None:
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

    delete_response = client.delete(
        f"/recipes/{recipe_id}/ingredients/{banana['id']}",
        headers={"X-API-Key": "dev-secret-key"},
    )

    assert delete_response.status_code == 204

    nutrition_response = client.get(f"/recipes/{recipe_id}/nutrition")
    assert nutrition_response.status_code == 200
    assert nutrition_response.json()["total"]["calories"] == 120.0
