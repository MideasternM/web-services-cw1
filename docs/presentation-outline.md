# Presentation Script and Slide Outline

## Slide 1: Title and Project Aim

**Title:** Nutrition and Recipe Analytics API

**What to say:**  
This project is a FastAPI and SQLite web service for managing recipes and ingredients and for calculating nutrition summaries from stored data. I chose this topic because it allows me to demonstrate both standard CRUD functionality and analytical features in a single API.

## Slide 2: Why This Project

**On slide:**
- Data-driven API
- SQL-backed CRUD
- Relational design
- Nutrition analytics

**What to say:**  
I wanted a project that went beyond a basic single-table CRUD application. Recipe and nutrition data is a good fit because it naturally requires relationships between entities, and it also allows meaningful analytics such as calorie totals and category statistics.

## Slide 3: Technology Stack

**On slide:**
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest

**What to say:**  
I selected FastAPI because this coursework is API-oriented and FastAPI gives strong validation and automatic OpenAPI documentation. SQLite was chosen for simple and reliable local execution. SQLAlchemy models the database structure, Pydantic validates requests and responses, and pytest provides repeatable automated verification.

## Slide 4: Architecture

**On slide:**
- Routers
- Models
- Schemas
- Services
- Database layer

**What to say:**  
The application is split into focused modules. Routers manage HTTP requests, models define persistent entities, schemas handle validation, and services contain derived logic such as nutrition calculation. This separation keeps the code modular and easier to explain and test.

## Slide 5: Database Design

**On slide:**
- `recipes`
- `ingredients`
- `recipe_ingredients`

**What to say:**  
The central design choice is the many-to-many relationship between recipes and ingredients. Instead of storing nutrition totals directly in a recipe, the API calculates totals from ingredient nutrition values and quantities. This avoids duplication and better reflects relational database design.

## Slide 6: API Features

**On slide:**
- Recipe CRUD
- Ingredient CRUD
- Add/remove ingredient links
- Search
- Nutrition summary
- Category analytics

**What to say:**  
The API includes full CRUD for both recipes and ingredients. In addition, it supports linking ingredients to recipes, removing those links, searching recipes, calculating nutrition summaries, and counting recipes by category. This extends the project beyond the minimum coursework requirements.

## Slide 7: Security and Error Handling

**On slide:**
- API key protection on writes
- `401`, `404`, `422`
- Consistent JSON error structure

**What to say:**  
All write operations are protected by an API key sent through the request header. This is a lightweight form of authentication that fits the coursework scope. The API also returns appropriate HTTP status codes and structured error responses for missing resources, validation problems, and unauthorized requests.

## Slide 8: Testing and Verification

**On slide:**
- 15 automated tests
- CRUD coverage
- Analytics coverage
- Isolated SQLite test database

**What to say:**  
Testing was an important part of the implementation. The test suite currently includes fifteen passing tests covering health checks, CRUD behaviour, authentication, analytics, search, and link removal. I also used a separate SQLite test database so that the tests remain repeatable and isolated from development data.

## Slide 9: Demo Plan

**On slide:**
- Show repository
- Show README and commit history
- Open `/docs`
- Create a recipe
- Add ingredients
- Show nutrition and analytics

**What to say:**  
In the demonstration I would first show the repository and README, then open the generated API docs. After that I would create a recipe with the API key, link ingredients, and show the nutrition endpoint and the category analytics endpoint. This gives a clear flow from data entry to derived results.

## Slide 10: Reflection and Future Work

**On slide:**
- Route ordering issue
- Testing benefits
- JWT auth
- Richer analytics
- PostgreSQL deployment

**What to say:**  
One technical issue I encountered was a route conflict between `/recipes/search` and the dynamic recipe identifier route. Solving that highlighted the importance of route design in FastAPI. If I continued the project, I would replace the API key with JWT-based authentication, expand the analytics and search features, and move from SQLite to PostgreSQL for a stronger deployment story.

## Slide 11: GenAI Usage

**On slide:**
- Planning
- Design exploration
- Debugging support
- Documentation drafting

**What to say:**  
I used generative AI throughout the project for planning, architecture exploration, debugging support, and drafting documentation. However, the final technical decisions, scope control, and review of outputs remained my responsibility. Representative conversation logs will be included in the final submission appendix.
