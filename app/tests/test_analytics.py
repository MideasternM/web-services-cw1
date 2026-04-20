from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_recipe_category_analytics_returns_counts() -> None:
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
