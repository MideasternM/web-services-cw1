from pathlib import Path
import zipfile


def test_pptx_file_exists() -> None:
    output = Path("slides/output/nutrition-api-deck.pptx")
    assert output.exists()


def test_pptx_contains_seven_slides() -> None:
    output = Path("slides/output/nutrition-api-deck.pptx")
    with zipfile.ZipFile(output) as archive:
        slide_names = [
            name
            for name in archive.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        ]
    assert len(slide_names) == 7
