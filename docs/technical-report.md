# Technical Report Draft

## 1. Project Overview

This project implements a Nutrition and Recipe Analytics API using FastAPI and SQLite. The aim is to provide a data-driven web service that supports CRUD operations for recipes and ingredients while also offering nutrition aggregation and category-based analytics. The project was designed for XJCO3011 Coursework 1 and therefore prioritises clear API design, SQL-backed persistence, lightweight authentication, testability, and a structure suitable for oral presentation.

## 2. Technology Stack Justification

FastAPI was selected because the coursework is explicitly API-focused. It provides clear request and response modelling, automatic validation, and built-in OpenAPI documentation through Swagger UI. SQLite was chosen because it keeps the project lightweight and reliable for local demonstration while still satisfying the coursework requirement for a SQL database. SQLAlchemy was used to model relational entities and support structured queries, and pytest was used to demonstrate a repeatable testing approach.

## 3. Architecture and Data Design

The project follows a layered structure with routers, models, schemas, services, and database utilities separated into different modules. This improves readability and makes the design easier to explain in the oral exam. The database design uses three main entities: `recipes`, `ingredients`, and `recipe_ingredients`. This allows the system to represent many-to-many relationships and compute recipe nutrition based on ingredient quantities rather than hardcoded values.

## 4. API Design

The API supports CRUD operations for recipes and ingredients, plus two relationship endpoints to add and remove ingredients from recipes. Read operations are public, while write operations are protected using an API key header. This approach introduces authentication without over-expanding the project into full user management. In addition to CRUD, the API provides a nutrition endpoint for per-recipe aggregation and an analytics endpoint for counting recipes by category.

## 5. Testing Approach

The implementation was built incrementally with test-first development. pytest and FastAPI's `TestClient` were used to validate endpoint behaviour. The test suite covers health checks, missing-resource handling, authentication, recipe CRUD, ingredient CRUD, nutrition calculations, search behaviour, category analytics, and ingredient removal from recipes. A dedicated SQLite test database is used during tests so that data is isolated and reproducible.

## 6. Challenges and Lessons Learned

One implementation issue emerged around route ordering in FastAPI. Initially, `/recipes/search` conflicted with the dynamic `/{recipe_id}` route, causing the request to be interpreted incorrectly and return a validation error. Reordering the static route before the dynamic route resolved the problem. This highlighted the importance of route specificity in API frameworks. Another useful lesson was the value of keeping database access behind dependency injection, which made it straightforward to swap to a test database during automated testing.

## 7. Limitations and Future Work

The current system uses a hardcoded API key and SQLite for simplicity. In a more advanced version, authentication could be replaced with JWT-based user accounts and role-based access control. Search could also be extended to include maximum calories and allergen exclusion using richer joins and aggregation queries. If the project were deployed beyond local coursework use, PostgreSQL would be a more suitable production database.

## 8. Version Control and Documentation

The repository maintains a visible commit history that shows the API being built incrementally. The README provides setup, testing, and run instructions, while the API documentation is available both through FastAPI's `/docs` endpoint and the Markdown document prepared for conversion to PDF. This structure supports both the coursework deliverables and the oral presentation flow.

## 9. Generative AI Declaration

Generative AI was used throughout the project for planning, architecture exploration, implementation sequencing, and revision of technical documentation. The AI was used to compare stack choices, shape the API design, and accelerate implementation under a controlled development process. Final technical decisions, scope choices, and review of outputs remained the responsibility of the student. Conversation logs and usage examples should be attached as appendix material in the submitted version.
