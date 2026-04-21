from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_empty_ingredient_list_returns_empty_items() -> None:
    response = client.get("/ingredients")

    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_create_ingredient_rejects_negative_nutrition() -> None:
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


def test_update_ingredient_changes_values() -> None:
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


def test_delete_ingredient_returns_204() -> None:
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


def test_delete_linked_ingredient_cascades_and_nutrition_still_works() -> None:
    recipe = client.post(
        "/recipes",
        json={
            "name": "Fruit Bowl",
            "description": "Simple fruit bowl",
            "category": "breakfast",
            "difficulty": "easy",
            "servings": 2,
            "instructions": "Mix and serve",
        },
        headers={"X-API-Key": "dev-secret-key"},
    ).json()

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
        f"/recipes/{recipe['id']}/ingredients",
        json={"ingredient_id": yogurt["id"], "quantity_g": 200},
        headers={"X-API-Key": "dev-secret-key"},
    )
    client.post(
        f"/recipes/{recipe['id']}/ingredients",
        json={"ingredient_id": banana["id"], "quantity_g": 100},
        headers={"X-API-Key": "dev-secret-key"},
    )

    delete_response = client.delete(f"/ingredients/{banana['id']}", headers={"X-API-Key": "dev-secret-key"})
    assert delete_response.status_code == 204

    nutrition_response = client.get(f"/recipes/{recipe['id']}/nutrition")
    assert nutrition_response.status_code == 200
    assert nutrition_response.json()["total"]["calories"] == 120.0
