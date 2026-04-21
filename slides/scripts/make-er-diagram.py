from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slides" / "assets" / "er-diagram.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_table(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, rows: list[str], fill: str) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill=fill, outline="#D7DEE3", width=3)
    draw.rounded_rectangle((x1, y1, x2, y1 + 70), radius=24, fill="#132238")
    draw.rectangle((x1, y1 + 46, x2, y1 + 70), fill="#132238")
    draw.text((x1 + 28, y1 + 20), title, fill="white", font=font(28, True))
    y = y1 + 96
    for row in rows:
        draw.text((x1 + 26, y), row, fill="#18212B", font=font(21))
        y += 34


def main() -> None:
    image = Image.new("RGB", (1600, 900), "#F4F7F8")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, 1600, 120), fill="#132238")
    draw.text((60, 34), "Entity relationship model", fill="white", font=font(46, True))
    draw.text((60, 82), "Recipes and ingredients are linked through a quantity-bearing join table", fill="#D9EEF2", font=font(24))

    recipe_box = (80, 210, 480, 610)
    join_box = (600, 260, 1000, 560)
    ingredient_box = (1120, 210, 1520, 610)

    draw_table(
        draw,
        recipe_box,
        "recipes",
        [
            "PK  id",
            "name",
            "category",
            "difficulty",
            "servings",
            "instructions",
            "created_at",
            "updated_at",
        ],
        "#FFFFFF",
    )
    draw_table(
        draw,
        join_box,
        "recipe_ingredients",
        [
            "PK  id",
            "FK  recipe_id -> recipes.id",
            "FK  ingredient_id -> ingredients.id",
            "quantity_g",
            "UNIQUE(recipe_id, ingredient_id)",
        ],
        "#EAF4F6",
    )
    draw_table(
        draw,
        ingredient_box,
        "ingredients",
        [
            "PK  id",
            "name",
            "calories_per_100g",
            "protein_per_100g",
            "fat_per_100g",
            "carbs_per_100g",
            "contains_allergen",
            "allergen_notes",
        ],
        "#FFFFFF",
    )

    draw.line((480, 410, 600, 410), fill="#137C8B", width=8)
    draw.line((1000, 410, 1120, 410), fill="#137C8B", width=8)
    draw.polygon([(586, 398), (586, 422), (610, 410)], fill="#137C8B")
    draw.polygon([(1106, 398), (1106, 422), (1130, 410)], fill="#137C8B")

    draw.text((500, 358), "1", fill="#137C8B", font=font(30, True))
    draw.text((540, 436), "many", fill="#516173", font=font(22, True))
    draw.text((1020, 358), "many", fill="#516173", font=font(22, True))
    draw.text((1068, 436), "1", fill="#137C8B", font=font(30, True))

    draw.rounded_rectangle((440, 700, 1160, 790), radius=20, fill="#DDF3E8", outline="#B8D8C6", width=3)
    draw.text((472, 726), "Nutrition is derived from ingredient quantities, so the join table is part of the business logic.", fill="#18212B", font=font(24, True))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)


if __name__ == "__main__":
    main()
