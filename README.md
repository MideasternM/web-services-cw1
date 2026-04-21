# Nutrition and Recipe Analytics API

This repository contains a FastAPI and SQLite coursework project for XJCO3011 Web Services and Web Data. The API supports CRUD operations for recipes and ingredients, lightweight API-key protection for write operations, and analytics endpoints for nutrition and category summaries.

## Stack

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Open the generated API docs at `http://127.0.0.1:8000/docs`.

## Authentication

Protected write endpoints require:

```http
X-API-Key: dev-secret-key
```

## Tests

```powershell
.\.venv\Scripts\python -m pytest app/tests -v
```

## Seed Data

```powershell
.\.venv\Scripts\python app\db\seed.py
```

## Project Deliverables

- Source code and commit history in this repository
- API documentation through FastAPI OpenAPI and `/docs`
- API documentation PDF: `docs/api-documentation.pdf`
- Technical report PDF: `docs/technical-report.pdf`
- Presentation deck: `slides/output/nutrition-api-deck.pptx`
- Presentation outline and speaking notes: `docs/presentation-outline.md`

## Presentation

Generated deck:
`slides/output/nutrition-api-deck.pptx`

Build notes:
`docs/presentation-build-notes.md`
