from app.config.settings import settings
from fastapi import FastAPI
from app.config.settings import settings
from app.api.document_routes import router as document_router


app = FastAPI(
    title="FinInsight AI",
    description="Enterprise Financial Document Intelligence Platform",
    version=settings.app_version,
)


@app.get("/")
def root():
    return {"message": "Welcome to FinInsight AI"}

app.include_router(document_router)

@app.get("/health")
def health():
    return {"status": "UP"}
