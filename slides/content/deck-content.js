module.exports = [
  {
    key: "title",
    title: "Nutrition and Recipe Analytics API",
    subtitle: "A FastAPI and SQLite data-driven web service with CRUD and nutrition analytics"
  },
  {
    key: "motivation",
    title: "Why This Project",
    bullets: [
      "Recipe and nutrition data supports both CRUD operations and analytical queries",
      "The domain naturally requires a relational design rather than a single flat table",
      "The project goes beyond minimum coursework requirements by combining operations with derived results"
    ]
  },
  {
    key: "stack_architecture",
    title: "Stack and Architecture",
    bullets: [
      "FastAPI, SQLite, SQLAlchemy, Pydantic, pytest",
      "Client requests flow through routers, schemas, services, models, and the database",
      "The modular structure improves maintainability and oral-exam explainability"
    ]
  },
  {
    key: "data_api",
    title: "Database Design and API Surface",
    bullets: [
      "Core entities: recipes, ingredients, recipe_ingredients",
      "API supports recipe CRUD, ingredient CRUD, link and unlink operations",
      "Search, nutrition summary, and category analytics extend the API beyond basic CRUD"
    ]
  },
  {
    key: "quality",
    title: "Security, Validation, and Testing",
    bullets: [
      "Write operations are protected with X-API-Key authentication",
      "Pydantic validates request data and status codes follow API conventions",
      "15 automated tests verify health, CRUD, search, analytics, and relationship behaviour"
    ]
  },
  {
    key: "demo_challenge",
    title: "Demo Flow and Technical Challenge",
    bullets: [
      "Show repository, README, commit history, and Swagger docs",
      "Create a recipe, add ingredients, and demonstrate nutrition plus analytics endpoints",
      "A route conflict between /recipes/search and /{recipe_id} was fixed by reordering routes"
    ]
  },
  {
    key: "conclusion",
    title: "Conclusion and Future Work",
    bullets: [
      "The project delivers SQL-backed CRUD, analytics, authentication, testing, and documentation",
      "Future work includes JWT authentication, richer analytics, and PostgreSQL deployment",
      "GenAI was used transparently for planning, debugging support, and documentation drafting"
    ]
  }
];
