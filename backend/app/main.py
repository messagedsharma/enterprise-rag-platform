from fastapi import FastAPI

app = FastAPI(
    title="FinInsight AI",
    description="Enterprise Financial Document Intelligence Platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to FinInsight AI"}


@app.get("/health")
def health():
    return {"status": "UP"}
