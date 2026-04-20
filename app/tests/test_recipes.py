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
