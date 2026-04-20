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
