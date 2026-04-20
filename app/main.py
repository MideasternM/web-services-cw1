from fastapi import FastAPI


app = FastAPI(title="Nutrition and Recipe Analytics API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
