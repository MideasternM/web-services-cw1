# Technical Report

## 1. Introduction

This project implements a Nutrition and Recipe Analytics API for the XJCO3011 Web Services and Web Data coursework. The main objective was to build a data-driven web service that satisfies the core coursework requirements while still demonstrating design decisions beyond a minimum CRUD application. To achieve this, the project supports SQL-backed CRUD operations for recipes and ingredients, models many-to-many relationships between recipes and ingredients, and exposes analytical functionality that calculates nutrition summaries and category-level statistics.

The project was intentionally scoped around nutrition and recipe data because this domain naturally supports both transactional operations and analytical queries. A simple single-table application would have been sufficient for a pass-level submission, but it would not have demonstrated much database design or API reasoning. In contrast, the chosen design makes it possible to explain relational modelling, validation, authentication, testing strategy, and endpoint structure in a way that is technically defensible during the oral examination.

## 2. Technology Stack and Rationale

FastAPI was chosen as the backend framework because the coursework is explicitly centred on web services rather than server-rendered pages. FastAPI provides strong request and response modelling, built-in validation, automatic documentation through OpenAPI, and a development workflow that is well aligned with an API-focused coursework submission. This made it easier to keep the implementation consistent with the documented interface and reduced the risk of undocumented behaviour appearing in the final system.

SQLite was selected as the database because it satisfies the SQL requirement while keeping local execution simple and reliable. For a coursework project that must be demonstrated live, reduced operational complexity is a practical advantage. SQLAlchemy was used to define database models and support relational queries, while Pydantic was used for schema validation and response serialization. pytest was adopted as the testing framework because it integrates cleanly with FastAPI's test client and supports repeatable verification of endpoint behaviour.

The main trade-off in this stack is that SQLite and a hardcoded API key are not production-grade choices for a larger deployed service. However, these decisions were appropriate for the coursework context because they prioritized correctness, clarity, and ease of demonstration over production-scale infrastructure.

## 3. System Architecture and Data Model

The application follows a layered structure with separate modules for routers, schemas, models, services, and database configuration. This separation improves readability and allows each layer to have a clear responsibility. Routers define HTTP behaviour, models define persistent entities, schemas define validated inputs and outputs, and services contain derived logic such as nutrition aggregation. This structure was chosen to support maintainability and to make the architecture easier to explain in the presentation and question-and-answer session.

The database design is based on three entities: `recipes`, `ingredients`, and `recipe_ingredients`. The `recipes` table stores general recipe information such as name, category, difficulty, servings, and instructions. The `ingredients` table stores nutrition information per 100 grams, including calories, protein, fat, carbohydrates, and allergen metadata. The `recipe_ingredients` table models the many-to-many relationship between the two and records the quantity of each ingredient used in a particular recipe.

This design was important because recipe nutrition should not be stored as hardcoded totals. Instead, totals are calculated from ingredient values and quantities. That decision improves data consistency and makes the analytical endpoints meaningful. It also demonstrates a more realistic use of relational modelling than a flat CRUD structure would.

## 4. API Design and Functionality

The API exposes CRUD operations for recipes and ingredients, relationship management endpoints for linking and unlinking ingredients to recipes, and analytics endpoints for nutrition summaries and category counts. Public read endpoints are provided for browsing data, while write endpoints are protected with an API key passed through the `X-API-Key` header. This authentication model is intentionally lightweight. It introduces an access-control concept without expanding the project into full user registration and session management, which would have added complexity without improving alignment with the coursework goals.

The recipe endpoints support listing, search, retrieval by identifier, creation, update, and deletion. The ingredient endpoints provide the same CRUD structure. In addition, the API supports adding an ingredient to a recipe with a specified quantity and removing an existing recipe-ingredient link. These relationship endpoints were necessary to make the nutrition calculation meaningful because the API derives totals from stored composition data rather than directly entered totals.

Two analytical features were added to move the project beyond basic CRUD. The first is a nutrition summary endpoint that calculates total and per-serving calories, protein, fat, and carbohydrates for a given recipe. The second is a category analytics endpoint that counts recipes by category. A search endpoint was also included to support filtered retrieval by category, difficulty, and serving count. Together, these features help demonstrate that the API is both data-driven and analytically useful.

## 5. Testing and Verification

The implementation was developed incrementally with test-first behaviour for each major feature. pytest and FastAPI's `TestClient` were used to validate endpoint responses, status codes, authentication behaviour, and analytics calculations. A dedicated SQLite test database was configured so that tests could run in isolation from local development data. This was important because API tests that share state with manual usage are difficult to trust and difficult to repeat consistently.

The final test suite covers health checks, missing-resource handling, API key enforcement, recipe CRUD, ingredient CRUD, nutrition aggregation, recipe search, category analytics, and removal of ingredients from recipes. At the point of verification, the command `python -m pytest app/tests -v` produced fifteen passing tests. This matters for the coursework because the marking criteria explicitly reward evidence of testing and effective handling of errors, not just the presence of runnable endpoints.

## 6. Challenges and Lessons Learned

One concrete implementation issue arose around route matching. Initially, the static `/recipes/search` endpoint conflicted with the dynamic `/{recipe_id}` route, which caused the framework to interpret the string `search` as though it were a recipe identifier. The resulting validation failure showed that even small routing decisions can affect API correctness. Reordering the static route before the dynamic route resolved the issue and reinforced the importance of route specificity when designing REST APIs.

Another useful lesson was the value of dependency-based database access. By keeping database sessions behind a shared dependency function, it became straightforward to override the session during testing and point the application at a test-specific SQLite database. This reduced coupling between runtime configuration and test execution, and it made the test suite much more reliable. The project also highlighted the importance of building analytical behaviour on top of stable relational data rather than treating analytics as a separate, loosely connected feature.

## 7. Limitations and Future Work

The system has several deliberate limitations. Authentication is implemented with a single API key rather than a full user model, and SQLite is used instead of a more scalable production database such as PostgreSQL. Search functionality currently filters by simple recipe-level fields rather than performing richer aggregate filtering such as maximum calories or allergen exclusion across linked ingredients. In addition, the project has not yet been deployed to a remote hosting platform, although the repository and local execution flow are structured to support that next step.

Future improvements would therefore focus on three areas. First, authentication could be replaced with JWT-based user accounts and role-based permissions. Second, the search and analytics functionality could be expanded to support richer filtering and reporting over linked ingredient data. Third, the database layer could be migrated from SQLite to PostgreSQL to support a more production-oriented deployment story. These changes would strengthen the project further, but they were intentionally left outside the current scope in order to keep the implementation coherent and demonstrable within the coursework timeline.

## 8. Version Control, Documentation, and Submission Readiness

The repository has been developed with visible commit history so that the progression of the implementation can be inspected during marking. This is important because the coursework brief explicitly states that examiners will examine repository contents and commit history. The README provides setup instructions, run instructions, testing commands, authentication details, and seed-data usage. API documentation is available through FastAPI's generated OpenAPI interface and has also been captured in a Markdown document that can be converted into the required PDF submission format.

The supporting submission structure also includes a technical report draft and a presentation outline. This means the repository now contains the main components needed to continue toward final submission: runnable source code, automated tests, visible version control, API documentation content, report content, and presentation material. The remaining work is largely formatting and polishing rather than major backend implementation.

## 9. Generative AI Declaration

Generative AI was used as an active development aid across planning, architecture exploration, implementation sequencing, and documentation drafting. It was used to compare backend stack options, refine the project scope around a domain that could support both CRUD and analytics, structure the implementation into manageable milestones, and improve the written presentation of the design. AI assistance was also used during debugging and documentation review. Final judgement over scope, trade-offs, and acceptance of generated outputs remained with the student, and all AI use should be declared alongside representative conversation logs in the final submitted appendix.
