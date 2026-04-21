import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slides" / "assets" / "api-response-examples.png"
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import database as database_module
from app.db.database import Base
from app.main import app


API_KEY = {"X-API-Key": "dev-secret-key"}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/aptos-bold.ttf" if bold else "C:/Windows/Fonts/aptos.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_demo_data(client: TestClient) -> tuple[int, int]:
    recipe = client.post(
        "/recipes",
        headers=API_KEY,
        json={
            "name": "Protein Breakfast Bowl",
            "category": "Breakfast",
            "difficulty": "easy",
            "servings": 2,
            "instructions": "Combine yoghurt, oats, berries, and nuts.",
        },
    ).json()
    ingredient = client.post(
        "/ingredients",
        headers=API_KEY,
        json={
            "name": "Greek yoghurt",
            "calories_per_100g": 59,
            "protein_per_100g": 10.0,
            "fat_per_100g": 0.4,
            "carbs_per_100g": 3.6,
            "allergens": "milk",
        },
    ).json()
    client.post(
        f"/recipes/{recipe['id']}/ingredients",
        headers=API_KEY,
        json={"ingredient_id": ingredient["id"], "quantity_g": 250},
    )
    return recipe["id"], ingredient["id"]


def compact_json(value: object, max_chars: int = 470) -> str:
    text = json.dumps(value, indent=2, ensure_ascii=False)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 6].rstrip() + "\n  ..."


def capture_examples() -> list[tuple[str, int, object]]:
    demo_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=demo_engine)
    Base.metadata.create_all(bind=demo_engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[database_module.get_db] = override_get_db
    client = TestClient(app)
    try:
        recipe_id, _ = create_demo_data(client)
        requests = [
            ("GET /health", client.get("/health")),
            (f"GET /recipes/{recipe_id}/nutrition", client.get(f"/recipes/{recipe_id}/nutrition")),
            ("GET /analytics/recipes/by-category", client.get("/analytics/recipes/by-category")),
            (
                "POST /recipes without X-API-Key",
                client.post(
                    "/recipes",
                    json={
                        "name": "Unauthorized Example",
                        "category": "Demo",
                        "difficulty": "easy",
                        "servings": 1,
                        "instructions": "This request should be blocked.",
                    },
                ),
            ),
        ]
        return [(label, response.status_code, response.json()) for label, response in requests]
    finally:
        app.dependency_overrides.clear()


def status_color(status: int) -> str:
    if status < 300:
        return "#16A34A"
    if status < 500:
        return "#D97706"
    return "#DC2626"


def main() -> None:
    examples = capture_examples()
    image = Image.new("RGB", (1600, 1000), "#F4F7F8")
    draw = ImageDraw.Draw(image)
    title_font = font(48, True)
    body_font = font(26)
    mono_font = font(23)
    label_font = font(25, True)

    draw.rectangle((0, 0, 1600, 140), fill="#132238")
    draw.text((60, 38), "Real API response evidence", fill="white", font=title_font)
    draw.text((60, 96), "Generated from FastAPI TestClient using the implemented endpoints", fill="#D9EEF2", font=body_font)

    card_positions = [(60, 185), (830, 185), (60, 585), (830, 585)]
    for index, ((label, status, payload), (x, y)) in enumerate(zip(examples, card_positions)):
        fill = "#FFFFFF" if index % 2 == 0 else "#FDFEFE"
        draw.rounded_rectangle((x, y, x + 710, y + 340), radius=26, fill=fill, outline="#D7DEE3", width=3)
        draw.text((x + 34, y + 30), label, fill="#18212B", font=label_font)
        draw.rounded_rectangle((x + 520, y + 24, x + 660, y + 70), radius=18, fill=status_color(status))
        draw.text((x + 555, y + 35), str(status), fill="white", font=label_font)

        json_text = compact_json(payload)
        draw.rounded_rectangle((x + 34, y + 92, x + 676, y + 305), radius=16, fill="#132238")
        line_y = y + 118
        for line in json_text.splitlines()[:8]:
            draw.text((x + 58, line_y), line, fill="#D9EEF2", font=mono_font)
            line_y += 26

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)


if __name__ == "__main__":
    main()
