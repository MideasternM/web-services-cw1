module.exports = [
  {
    key: "title",
    title: "Nutrition and Recipe Analytics API",
    subtitle: "FastAPI + SQLite coursework project with CRUD, derived nutrition analytics, automated testing, and submission-ready deliverables",
    kicker: "XJCO3011 Web Services and Web Data",
    presenter: "Shuyu Cao",
  },
  {
    key: "problem_context",
    title: "Why This Project Is More Than Basic CRUD",
    label: "PROJECT SCOPE",
    headline: "A recipe API is a good coursework domain because it needs both transactions and calculation.",
    bullets: [
      "Recipes and ingredients form a real many-to-many relational model.",
      "Nutrition totals are derived from linked ingredient quantities rather than typed in manually.",
      "The API can demonstrate CRUD, validation, authentication, and analytics in one coherent system.",
    ],
  },
  {
    key: "architecture",
    title: "Architecture and Technology Stack",
    label: "SYSTEM DESIGN",
    stack: ["FastAPI", "SQLite", "SQLAlchemy", "Pydantic", "pytest"],
    flow: ["Client", "Routers", "Schemas", "Services", "Models", "SQLite"],
    notes: [
      "FastAPI provides typed endpoints and automatic OpenAPI documentation.",
      "The layered structure makes the code easier to explain, test, and extend.",
    ],
  },
  {
    key: "data_api",
    title: "Database Design and API Surface",
    label: "RELATIONAL MODEL",
    entities: [
      { name: "recipes", desc: "recipe metadata, category, difficulty, servings, instructions" },
      { name: "ingredients", desc: "nutrition values per 100g and allergen metadata" },
      { name: "recipe_ingredients", desc: "join table storing quantity_g for each recipe ingredient" },
    ],
    endpoints: [
      "CRUD: /recipes",
      "CRUD: /ingredients",
      "Search: /recipes/search",
      "Links: /recipes/{id}/ingredients",
      "Nutrition: /recipes/{id}/nutrition",
      "Analytics: /analytics/by-category",
    ],
  },
  {
    key: "quality",
    title: "Security, Validation, and Testing",
    label: "ENGINEERING QUALITY",
    stats: [
      { value: "15", caption: "automated tests" },
      { value: "401", caption: "unauthorized writes blocked" },
      { value: "422", caption: "schema validation errors" },
    ],
    bullets: [
      "Write endpoints require the X-API-Key header.",
      "Pydantic validates payload shape and data types before business logic runs.",
      "Tests cover CRUD, search, analytics, nutrition aggregation, and relationship removal.",
    ],
  },
  {
    key: "api_docs",
    title: "API Documentation Overview",
    label: "DELIVERABLE 1",
    highlights: [
      "Real browser screenshot of Swagger UI at /docs for live demonstration.",
      "API documentation was also exported into a separate PDF deliverable.",
      "Response evidence includes authentication, health, nutrition summaries, and analytics output.",
    ],
    callouts: ["Real /docs screenshot", "api-documentation.pdf", "Live JSON responses"],
  },
  {
    key: "version_control",
    title: "Version Control and Deliverables",
    label: "DELIVERABLES",
    commits: [
      "feat: complete recipe crud operations",
      "feat: add recipe nutrition analytics",
      "feat: add analytics endpoints and project documentation",
      "docs: refine report and presentation materials",
    ],
    deliverables: [
      "Public GitHub repository with visible commit history",
      "README with setup, run, seed, and test instructions",
      "API documentation PDF, technical report PDF, and presentation deck",
    ],
  },
  {
    key: "demo_report",
    title: "Demo Flow and Technical Report Highlights",
    label: "ORAL EXAM FLOW",
    demoSteps: [
      "Open GitHub repository and README",
      "Show commit history and project deliverables",
      "Open Swagger /docs",
      "Create recipe, link ingredients, show nutrition and category analytics",
    ],
    reportPoints: [
      "Rationale for choosing FastAPI, SQLite, and a layered design",
      "Testing approach, route-conflict lesson, limitations, and future work",
      "GenAI declaration included transparently in the report",
    ],
  },
  {
    key: "conclusion",
    title: "Technical Report Highlights and Q&A Readiness",
    label: "CONCLUSION",
    outcome: "The project satisfies the coursework brief with a runnable SQL-backed API, visible version history, documentation, testing evidence, and a defensible architecture.",
    future: [
      "Upgrade from API key auth to JWT-based authentication",
      "Expand analytics and richer recipe filtering",
      "Move from SQLite to PostgreSQL for a stronger deployment story",
    ],
    genai: "GenAI was used for planning, debugging support, and documentation drafting, with final technical decisions kept under student control.",
  },
];
