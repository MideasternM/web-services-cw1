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
