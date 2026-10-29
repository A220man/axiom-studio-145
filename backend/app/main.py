from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api.health import router as health_router

app = FastAPI(
    title="Axiom Studio 145",
    description="The agent harness performance optimization system",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")


@app.get("/")
async def root():
    return {"name": "Axiom Studio 145", "version": "0.1.0"}
