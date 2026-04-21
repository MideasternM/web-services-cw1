from pathlib import Path
import subprocess
import sys
import zipfile


TESTS_DIR = Path(__file__).resolve().parent
SLIDES_DIR = TESTS_DIR.parent
OUTPUT = SLIDES_DIR / "output" / "nutrition-api-deck.pptx"
ASSETS_DIR = SLIDES_DIR / "assets"


def test_pptx_file_exists() -> None:
    assert OUTPUT.exists()


def test_required_visual_assets_exist() -> None:
    assert (ASSETS_DIR / "swagger-ui-screenshot.png").exists()
    assert (ASSETS_DIR / "api-response-examples.png").exists()


def test_pptx_contains_seven_slides() -> None:
    with zipfile.ZipFile(OUTPUT) as archive:
        slide_names = [
            name
            for name in archive.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        ]
    assert len(slide_names) == 9


def test_pptx_core_title_is_set() -> None:
    with zipfile.ZipFile(OUTPUT) as archive:
        core_xml = archive.read("docProps/core.xml").decode("utf-8")
    assert "Nutrition and Recipe Analytics API" in core_xml


def test_extracted_deck_text_contains_core_sections() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", str(OUTPUT)],
        check=True,
        capture_output=True,
        text=True,
    )
    text = result.stdout
    assert "Nutrition and Recipe Analytics API" in text
    assert "Security, Validation, and Testing" in text
    assert "Version Control and Deliverables" in text
    assert "API Documentation Overview" in text
    assert "Technical Report Highlights" in text
    assert "Technical Report Highlights and Q&A Readiness" in text
