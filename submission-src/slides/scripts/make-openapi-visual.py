from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slides" / "assets" / "openapi-overview.png"
sys.path.insert(0, str(ROOT))

from app.main import app

COLORS = {
    "bg": "#f8fbfc",
    "ink": "#18212b",
    "muted": "#516173",
    "border": "#d7dee3",
    "green": "#ddf3e8",
    "blue": "#d9eef2",
    "amber": "#f7e6c7",
    "teal": "#137c8b",
    "navy": "#132238",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


METHOD_FILL = {
    "GET": COLORS["blue"],
    "POST": COLORS["green"],
    "PUT": COLORS["amber"],
    "DELETE": "#f5dbd8",
}


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str = COLORS["border"]) -> None:
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=2)


def main() -> None:
    schema = app.openapi()
    routes = []
    for path, methods in schema["paths"].items():
        for method in methods.keys():
            routes.append((method.upper(), path))

    preferred = [
        ("GET", "/health"),
        ("GET", "/recipes"),
        ("GET", "/recipes/search"),
        ("POST", "/recipes"),
        ("POST", "/recipes/{recipe_id}/ingredients"),
        ("GET", "/recipes/{recipe_id}/nutrition"),
        ("GET", "/analytics/recipes/by-category"),
    ]
    ordered = [item for item in preferred if item in routes]

    image = Image.new("RGB", (1400, 900), COLORS["bg"])
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, 1400, 116), fill=COLORS["navy"])
    draw.text((56, 34), "OpenAPI /docs overview", fill="white", font=font(42, True))
    draw.text((56, 84), "FastAPI-generated API documentation used for live demonstration", fill="#d9eef2", font=font(24))

    y = 160
    for method, path in ordered:
        rounded(draw, (58, y, 1342, y + 74), "white")
        draw.rounded_rectangle((86, y + 17, 194, y + 57), radius=10, fill=METHOD_FILL.get(method, COLORS["blue"]))
        draw.text((111, y + 26), method, fill=COLORS["ink"], font=font(18, True), anchor="mm")
        draw.text((226, y + 18), path, fill=COLORS["ink"], font=font(28, True))
        summary = {
            "/health": "health check",
            "/recipes": "list or create recipes",
            "/recipes/search": "filter by category, difficulty, and max servings",
            "/recipes/{recipe_id}/ingredients": "link ingredient quantity to recipe",
            "/recipes/{recipe_id}/nutrition": "derive nutrition summary from linked ingredients",
            "/analytics/recipes/by-category": "category-level analytics",
        }.get(path, "documented endpoint")
        draw.text((226, y + 47), summary, fill=COLORS["muted"], font=font(20))
        y += 86

    rounded(draw, (58, 780, 1342, 852), COLORS["green"], outline="#b8d8c6")
    draw.text(
        (86, 800),
        "Documentation evidence: endpoints, schemas, status codes, request bodies,",
        fill=COLORS["ink"],
        font=font(24),
    )
    draw.text(
        (86, 828),
        "and JSON responses are visible in /docs and captured in api-documentation.pdf.",
        fill=COLORS["ink"],
        font=font(24),
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
