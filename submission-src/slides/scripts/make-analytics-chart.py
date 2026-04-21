from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slides" / "assets" / "category-analytics-chart.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def main() -> None:
    data = [("breakfast", 2), ("lunch", 1)]
    image = Image.new("RGB", (1200, 760), "#f8fbfc")
    draw = ImageDraw.Draw(image)

    draw.text((54, 42), "Category analytics", fill="#18212b", font=font(44, True))
    draw.text((54, 96), "Example output from GET /analytics/recipes/by-category", fill="#516173", font=font(24))

    axis_left = 220
    axis_bottom = 620
    max_width = 780
    max_value = max(value for _, value in data)
    colors = ["#137c8b", "#f7c66a"]

    draw.line((axis_left, 188, axis_left, axis_bottom), fill="#9aa8b3", width=3)
    draw.line((axis_left, axis_bottom, axis_left + max_width + 70, axis_bottom), fill="#9aa8b3", width=3)

    for index, (category, value) in enumerate(data):
        y = 250 + index * 160
        bar_width = int(max_width * value / max_value)
        draw.text((54, y + 20), category, fill="#18212b", font=font(30, True))
        draw.rounded_rectangle((axis_left, y, axis_left + bar_width, y + 74), radius=18, fill=colors[index])
        draw.text((axis_left + bar_width + 28, y + 18), str(value), fill="#18212b", font=font(34, True))
        draw.text((axis_left, y + 90), f"{value} recipe{'s' if value != 1 else ''}", fill="#516173", font=font(22))

    draw.rounded_rectangle((54, 660, 1128, 724), radius=18, fill="#ddf3e8", outline="#b8d8c6", width=2)
    draw.text((82, 680), "The chart shows that the API returns derived grouped data, not only individual CRUD records.", fill="#18212b", font=font(24))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
