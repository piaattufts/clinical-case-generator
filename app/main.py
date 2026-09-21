"""FastAPI application. Phase 1 exposes a health check only."""

from fastapi import FastAPI

from app import __version__

app = FastAPI(title="Clinical Case Generator", version=__version__)


@app.get("/health")
def health() -> dict[str, str]:
    """Process liveness. This does not check the database."""
    return {"status": "ok"}
