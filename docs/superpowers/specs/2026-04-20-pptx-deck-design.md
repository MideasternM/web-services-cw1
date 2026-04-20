# Nutrition and Recipe Analytics API PPTX Deck Design

**Goal:** Create an English `.pptx` slide deck for the XJCO3011 oral examination that presents the Nutrition and Recipe Analytics API clearly within a five-minute presentation window.

**Target outcome:** A seven-slide academic presentation that balances oral-exam clarity with stronger visual quality than a basic classroom slide deck.

## 1. Presentation Context

The deck supports a ten-minute oral examination consisting of approximately five minutes of presentation and five minutes of question-and-answer discussion. The slides must therefore be optimized for short-form spoken delivery rather than dense, self-contained reading. The primary use case is that the presenter talks through the system while examiners visually confirm architecture, design quality, testing evidence, and delivery readiness.

## 2. Design Strategy

The presentation will use a seven-slide format instead of a longer ten-slide structure. This is a deliberate compression strategy to fit the five-minute delivery window more naturally. The deck should feel academically serious and technically polished, but it should avoid the look of a startup sales deck or a generic AI-generated bullet presentation.

The visual direction should be "academic but polished":

- dark navy, slate, and off-white as the core palette
- title and closing slides on dark backgrounds
- middle content slides on light backgrounds
- diagrams, cards, and structured visual blocks instead of dense bullet walls
- restrained accent color usage
- strong alignment and spacing

## 3. Slide Structure

### Slide 1: Title and Project Aim

Purpose:

- establish the project identity immediately
- show module context
- state the project in one sentence

Content:

- project title: `Nutrition and Recipe Analytics API`
- module name: `XJCO3011 Web Services and Web Data`
- student name placeholder
- subtitle describing FastAPI, SQLite, CRUD, and analytics

Visual approach:

- dark background
- large title
- small subtitle block
- subtle abstract technical background or geometric pattern

### Slide 2: Motivation and Problem Framing

Purpose:

- explain why this topic was selected
- justify why the project is more substantial than a trivial CRUD system

Content:

- recipe and nutrition data supports both transactions and analytics
- relational design is meaningful because recipes and ingredients form a many-to-many model
- the project goes beyond a single-table API

Visual approach:

- one central three-stage diagram: input data -> relational storage -> analytics output
- minimal supporting text

### Slide 3: Technology Stack and Architecture

Purpose:

- explain how the system is built
- show separation of concerns

Content:

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- client request flow through routers, schemas, services, models, and database

Visual approach:

- left side: compact stack cards
- right side: architecture flow diagram
- use arrows to show request and response movement

### Slide 4: Database Design and API Surface

Purpose:

- explain the database model
- show API breadth without listing too many raw endpoints

Content:

- `recipes`
- `ingredients`
- `recipe_ingredients`
- recipe CRUD
- ingredient CRUD
- link and unlink ingredient endpoints
- search endpoint
- nutrition endpoint
- category analytics endpoint

Visual approach:

- left or center: ER-style relationship diagram
- right: grouped API capability blocks
- emphasize that nutrition is computed from linked ingredient quantities

### Slide 5: Security, Validation, and Testing

Purpose:

- demonstrate engineering quality
- support higher-band marking criteria

Content:

- API key on write operations
- Pydantic validation
- status codes: `200`, `201`, `204`, `401`, `404`, `422`
- automated test coverage
- `15 passed`

Visual approach:

- split layout
- one side for security and validation
- one side for testing evidence
- include a compact terminal-style test result callout

### Slide 6: Demo Flow and Technical Challenge

Purpose:

- show how the live presentation would run
- include one concrete implementation lesson for Q&A strength

Content:

- repository
- README and commit history
- Swagger `/docs`
- create recipe
- add ingredients
- show nutrition endpoint
- show category analytics
- challenge: `/recipes/search` conflicting with `/{recipe_id}`
- solution: place static route before dynamic route

Visual approach:

- left half: demo flow as numbered sequence
- right half: issue/fix mini-diagram

### Slide 7: Conclusion, Future Work, and GenAI Declaration

Purpose:

- close clearly
- connect the project back to marking criteria
- declare AI usage transparently

Content:

- project delivers SQL-backed CRUD plus analytics
- modular architecture, auth, testing, and documentation are all present
- future work: JWT auth, richer search and analytics, PostgreSQL deployment
- GenAI used for planning, design exploration, debugging support, and documentation drafting

Visual approach:

- dark closing slide
- concise summary blocks
- one small "next steps" section
- one compact AI usage statement

## 4. Speaker Constraints

Each slide must support spoken delivery rather than replace it. The presenter should be able to spend approximately:

- 30-40 seconds on slide 1
- 35-40 seconds on slide 2
- 40-45 seconds on slide 3
- 45 seconds on slide 4
- 40-45 seconds on slide 5
- 45-50 seconds on slide 6
- 35-40 seconds on slide 7

This totals roughly five minutes with minor variation.

## 5. Build Requirements

The output should be a `.pptx` file created from scratch rather than manually assembled from an external template. The deck should use the installed `pptx` skill workflow and create a real PowerPoint file that can be opened locally. The file should be presentation-ready, but it does not need to include animations or advanced transitions.

## 6. Quality Bar

The finished deck should satisfy these conditions:

- clear enough for a five-minute oral exam
- visually stronger than a default white-background bullet deck
- technically accurate to the implemented repository
- consistent with the written report and API documentation
- realistic to present without rushing

## 7. Scope Boundary

This design is intentionally limited to one seven-slide deck. It does not include alternate visual themes, multiple deck variants, or a fully separate handout version. Once this design is approved, the next step is to generate the `.pptx` file itself.
