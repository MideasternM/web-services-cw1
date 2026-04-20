# Presentation Outline

## Slide 1: Project Overview

- Project title: Nutrition and Recipe Analytics API
- Module: XJCO3011 Web Services and Web Data
- Goal: CRUD plus analytics on nutrition data

## Slide 2: Why This Topic

- Chosen because it naturally supports relational data
- Suitable for CRUD and analytics in one API
- Easy to demonstrate with realistic examples

## Slide 3: Architecture and Stack

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- Lightweight API key authentication

## Slide 4: Database Design

- `recipes`
- `ingredients`
- `recipe_ingredients`
- Explain why the relationship table is needed

## Slide 5: API Endpoints

- Recipe CRUD
- Ingredient CRUD
- Link and unlink ingredient endpoints
- Nutrition summary endpoint
- Category analytics endpoint
- Search endpoint

## Slide 6: Demo Flow

- Show GitHub repo and commit history
- Show README
- Open `/docs`
- Create recipe with API key
- Add ingredients
- Show nutrition calculation
- Show category analytics

## Slide 7: Testing and Error Handling

- 13 automated tests
- API key protection
- 404 and 422 handling
- Controlled local SQLite test database

## Slide 8: Reflection and Future Work

- Lessons from route ordering and testing
- Current limitations
- Future improvements: JWT auth, richer search, PostgreSQL deployment

## Slide 9: GenAI Usage

- How AI was used for planning, design, and implementation support
- What decisions remained student-owned
- Reference conversation logs in appendix
