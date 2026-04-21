# Presentation Build Notes

The current presentation is a 9-slide academic deck designed for a 5-minute oral presentation followed by Q&A. It uses two AI-generated visual assets in `slides/assets/` and diagram/card layouts for the remaining technical content.

## Generate the deck

From the project root:

```powershell
cd slides
npm install
node generate-deck.js
```

Generated file:

```text
slides/output/nutrition-api-deck.pptx
```

## Verify the deck

From the project root:

```powershell
.\.venv\Scripts\python -m pytest slides/tests/pptx_smoke_test.py -v
```

Optional text extraction check:

```powershell
.\.venv\Scripts\python -m markitdown slides/output/nutrition-api-deck.pptx
```

Rendered QA images can be exported through PowerPoint into `slides/output/rendered-final-*` when a visual spacing check is needed. These rendered folders are temporary and are ignored by git.

## Next step

Open the generated `.pptx` in PowerPoint and do a final manual review of spacing, wrapping, and visual hierarchy before using it in the oral examination.
