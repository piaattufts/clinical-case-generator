"""HTTP routers beyond the process health check.

Phase 2 mounts GET /reference/medications, /labs, /diagnoses, and /symptoms.
"""

from app.api.reference import router as reference_router

__all__ = ["reference_router"]
