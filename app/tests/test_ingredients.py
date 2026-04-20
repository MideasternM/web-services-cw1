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
