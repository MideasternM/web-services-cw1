# Presentation Build Notes

The current presentation is a 9-slide academic deck designed for a 5-minute oral presentation followed by Q&A. Its editable source files now live under `submission-src/slides/`, while the final submission deck is kept at `slides/nutrition-api-deck-updated.pptx`.

## Generate the deck

From the project root:

```powershell
cd submission-src\slides
npm install
node generate-deck.js
```

Generated file:

```text
slides/nutrition-api-deck.pptx
```

Current enhanced deck committed in the repository:

```text
slides/nutrition-api-deck-updated.pptx
```

## Verify the deck

From the project root:

```powershell
.\.venv\Scripts\python -m pytest submission-src/slides/tests/pptx_smoke_test.py -v
```

Optional text extraction check:

```powershell
.\.venv\Scripts\python -m markitdown slides/nutrition-api-deck-updated.pptx
```

Rendered QA images should be exported into a temporary location outside `slides/` when a visual spacing check is needed, because the `slides/` submission folder is reserved for the final `.pptx` only.

## Next step

Open the generated `.pptx` in PowerPoint and do a final manual review of spacing, wrapping, and visual hierarchy before using it in the oral examination.
