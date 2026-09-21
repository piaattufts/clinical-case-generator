"""FastAPI application. Phase 2 adds local reference search routes."""

from fastapi import FastAPI

from app import __version__
from app.api.reference import router as reference_router

app = FastAPI(title="Clinical Case Generator", version=__version__)
app.include_router(reference_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Process liveness. This does not check the database."""
    return {"status": "ok"}
