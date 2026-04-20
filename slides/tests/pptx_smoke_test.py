from pathlib import Path


def test_pptx_file_exists() -> None:
    output = Path("slides/output/nutrition-api-deck.pptx")
    assert output.exists()
