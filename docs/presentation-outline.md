# Presentation Outline and Speaking Notes

This outline matches the generated 9-slide deck at `slides/output/nutrition-api-deck.pptx`. It is designed for a concise 5-minute presentation, leaving the remaining oral-exam time for questions.

## Slide 1: Nutrition and Recipe Analytics API

**On slide:** FastAPI + SQLite coursework project with CRUD, derived nutrition analytics, automated testing, and submission-ready deliverables.

**What to say:**  
This project is a FastAPI and SQLite web service for managing recipes and ingredients. The key point is that it is not only a CRUD application. It also links ingredients to recipes and calculates nutrition summaries from stored ingredient quantities. That makes the system a good fit for demonstrating API design, relational modelling, validation, authentication, testing, and documentation in one coherent coursework project.

## Slide 2: Why This Project Is More Than Basic CRUD

**On slide:** Recipes and ingredients create a many-to-many relational model, and nutrition totals are derived rather than typed in manually.

**What to say:**  
I chose this domain because recipe data naturally needs relationships. A recipe can contain many ingredients, and an ingredient can appear in many recipes. The join table also stores quantity, which is what makes the analytics meaningful. This gives the project more technical depth than a single-table CRUD API because the API can demonstrate transactions, validation, relationship management, and calculated outputs.

## Slide 3: Architecture and Technology Stack

**On slide:** FastAPI, SQLite, SQLAlchemy, Pydantic, pytest; request flow from client to routers, schemas, services, models, and SQLite.

**What to say:**  
FastAPI was chosen because it supports typed API development and automatically generates OpenAPI documentation. SQLite keeps the project easy to run locally, while SQLAlchemy provides the ORM layer. Pydantic validates request and response data. The code is separated into routers, schemas, models, services, and database configuration so each layer has a clear responsibility and the system is easier to explain during Q&A.

## Slide 4: Database Design and API Surface

**On slide:** ER diagram for `recipes`, `ingredients`, and `recipe_ingredients`, representative endpoints, derived nutrition logic, and a grouped category analytics chart.

**What to say:**  
The database has three core tables. `recipes` stores recipe metadata, `ingredients` stores nutrition per 100 grams and allergen information, and `recipe_ingredients` connects them with a quantity in grams. The ER diagram is important because it shows that this is a real relational model rather than separate flat tables. Nutrition is calculated from this relationship rather than stored as fixed recipe totals, and the chart shows category analytics returning grouped data beyond individual CRUD records.

## Slide 5: Security, Validation, and Testing

**On slide:** `15` automated tests, `401` unauthorized writes blocked, `422` schema validation responses, and `15 passed`.

**What to say:**  
Write operations require the `X-API-Key` header, which gives the project lightweight access control without adding unnecessary user-management complexity. Pydantic validates payload shape and types before the service logic runs, producing `422` errors for invalid requests. The final backend test run has fifteen passing tests covering health checks, CRUD, authentication, search, analytics, nutrition aggregation, and relationship removal.

## Slide 6: API Documentation Overview

**On slide:** Real Swagger UI `/docs` screenshot, `api-documentation.pdf`, and real JSON response examples.

**What to say:**  
The API can be demonstrated live through FastAPI's generated Swagger UI at `/docs`. This is useful because the examiner can see routes, request bodies, response schemas, and status codes directly from the running application. The slide now uses a real browser screenshot rather than only a schema-generated mockup, and the response panel shows actual JSON returned from the implemented endpoints. I also prepared a separate API documentation PDF that records the main endpoints, authentication requirements, example request bodies, responses, and expected status codes.

## Slide 7: Version Control and Deliverables

**On slide:** Commit-history evidence, README, report PDF, API documentation PDF, and deck.

**What to say:**  
The repository contains the source code, README setup instructions, visible commit history, test suite, API documentation, technical report, and presentation deck. This matters because the coursework brief expects the repository and commit history to be inspected. The commit history also helps show how the work developed incrementally, rather than appearing as a single final upload.

## Slide 8: Demo Flow and Technical Report Highlights

**On slide:** Open repository, show README and commit history, open `/docs`, create a recipe, link ingredients, show nutrition and analytics.

**What to say:**  
The demo flow starts from the repository and README, then moves into the live Swagger docs. A good demonstration sequence is to create a recipe, add or inspect ingredients, link them with quantities, show the nutrition endpoint, and then show category analytics. The technical report supports this by explaining the stack rationale, layered design, testing approach, route-conflict lesson, limitations, future work, and GenAI declaration.

## Slide 9: Technical Report Highlights and Q&A Readiness

**On slide:** Key outcome, future work, GenAI declaration, and Q&A topics.

**What to say:**  
The final outcome is a runnable SQL-backed API with CRUD, relationship management, calculated nutrition analytics, authentication, validation, tests, documentation, and a presentation deck. Future improvements would include JWT authentication, richer analytics and filtering, and PostgreSQL for a stronger deployment path. GenAI was used for planning, debugging support, and documentation drafting, but the final scope, trade-offs, and acceptance of outputs remained under student control.
