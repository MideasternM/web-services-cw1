# PPT Generation Prompt

Create a polished academic PowerPoint deck for a university computer science oral assessment.

## Context

The project is called **Nutrition and Recipe Analytics API**.  
It is an individual coursework project for the module **XJCO3011 Web Services and Web Data**.  
The presentation is for a **10-minute oral examination**, with roughly **5 minutes presentation** and **5 minutes Q\&A**.  
The presentation should look professional, technically credible, and appropriate for a final-year or upper-level undergraduate computer science student.  
The style should be clean, modern, and academically serious. Do not make it look like a startup pitch deck or a flashy marketing deck.

## Goal of the deck

The deck must help the presenter explain:
- what the API does,
- why this topic was chosen,
- how the system is designed,
- how the database is structured,
- what the key endpoints are,
- how authentication, validation, and testing were handled,
- what was learned technically,
- and how GenAI was used appropriately and transparently.

The deck should make it easier for the student to score well on:
- content quality,
- technical explanation,
- presentation structure and clarity,
- visual quality,
- and Q\&A readiness.

## Technical project details to reflect accurately

Backend stack:
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest

Key features:
- CRUD for recipes
- CRUD for ingredients
- link ingredients to recipes with quantities
- remove ingredient links from recipes
- nutrition summary endpoint for each recipe
- category analytics endpoint
- recipe search endpoint
- API key authentication for write operations
- JSON error handling with appropriate status codes

Data model:
- recipes
- ingredients
- recipe_ingredients

Important technical points:
- recipe nutrition is calculated from ingredient quantities, not hardcoded
- static route `/recipes/search` originally conflicted with the dynamic recipe route and was fixed by route ordering
- automated tests exist and all tests pass
- there are currently 15 automated tests

## Required deck structure

Create exactly **9 slides**.  
Do not create fewer or more.

### Slide 1: Title Slide
Include:
- project title
- module name
- student name placeholder
- short subtitle such as: “A FastAPI and SQLite data-driven web service with CRUD and nutrition analytics”

Visual direction:
- minimal but polished
- subtle technical or data-themed background
- no clutter

### Slide 2: Problem and Motivation
Explain:
- why recipe and nutrition data is a good domain for a web API
- why this domain is more interesting than a trivial single-table CRUD system
- why it supports both operational and analytical endpoints

Visual:
- clean 3-part concept diagram: data input -> relational storage -> analytics output

### Slide 3: Technology Stack and System Architecture
Show the stack and application architecture with clearly labelled blocks:
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- routers
- schemas
- models
- services
- database layer

For each technology, briefly state why it was chosen.
Explain how responsibilities are separated and why this improves modularity and maintainability.

Visual:
- technology cards plus architecture flow diagram
- arrows showing request flow from client to router to service/model to database

### Slide 4: Database Design and API Surface
Show the relational design with:
- recipes
- ingredients
- recipe_ingredients

Explain:
- many-to-many relationship
- why quantity is stored in the join table
- why nutrition is derived instead of stored directly on the recipe
- representative endpoints for CRUD, relationship management, nutrition, search, and category analytics

Visual:
- ER diagram
- professional database-table style layout plus compact endpoint map

### Slide 5: Security, Validation, and Testing
Explain:
- API key authentication using `X-API-Key`
- validation with Pydantic
- use of standard status codes: 200, 201, 204, 401, 404, 422
- consistent JSON error structure
- automated testing with pytest and FastAPI TestClient
- isolated SQLite test database
- all 15 tests pass

Visual:
- request/response flow example
- small code-like example of an error JSON block
- clean terminal-output mockup showing `15 passed`

### Slide 6: API Documentation Overview
Explain:
- interactive Swagger UI is available at `/docs`
- API documentation is also exported as `api-documentation.pdf`
- examples include authentication, CRUD, nutrition summaries, and analytics output

Visual:
- Swagger/OpenAPI mockup
- documentation deliverable cards

### Slide 7: Version Control and Deliverables
Explain:
- visible commit history
- README setup, run, seed, and test instructions
- API documentation PDF
- technical report PDF
- presentation deck

Visual:
- commit-history timeline
- deliverables grid

### Slide 8: Demo Flow and Technical Report Highlights
Split this slide into two clear halves.

Left half:
- demo sequence:
  - show repository
  - show README and commit history
  - open `/docs`
  - create recipe
  - add ingredients
  - show nutrition endpoint
  - show category analytics

Right half:
- stack rationale
- testing approach
- route-conflict lesson
- limitations and future work
- GenAI declaration

Visual:
- left side step flow
- right side report-highlight cards

### Slide 9: Conclusion and GenAI Declaration
Summarize:
- what the project achieved
- why it meets and exceeds minimum coursework requirements
- likely future work: JWT auth, richer analytics, PostgreSQL deployment
- transparent GenAI usage for planning, debugging, design exploration, and documentation drafting

Visual:
- concise final summary panel
- optional small section called “Next steps”

## Design style requirements

Use a formal academic design language:
- white or very light background
- dark grey or near-black text
- one restrained accent color such as deep blue, dark green, or muted orange
- strong alignment and spacing
- high readability
- no childish icons
- no generic stock-photo feel
- no neon colors
- no cluttered diagrams
- avoid overly decorative transitions

Typography:
- modern, clean, serious
- bold section headings
- readable body text
- good visual hierarchy

Charts and diagrams:
- should look intentionally designed, not auto-generated default SmartArt
- must be consistent across slides
- use the same color palette and line weight throughout

## Slide density rules

- Each slide should have one central message.
- Keep text concise.
- Avoid large paragraphs on slides.
- Speaker explanation can be richer than visible slide text.
- Prefer diagrams, labeled blocks, tables, and short bullets.

## Speaker-support requirement

For each slide, also generate:
- a short speaker note paragraph of 60 to 120 words

The speaker notes should help the presenter explain the slide naturally in an oral exam.

## Output format

Generate the result as a slide-by-slide specification with:
- slide title
- exact on-slide text
- visual layout description
- speaker notes

The output should be detailed enough that another AI or a human designer can directly turn it into a polished PowerPoint without guessing.
