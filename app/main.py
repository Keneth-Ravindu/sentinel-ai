from fastapi import FastAPI

from app.api.incidents import router as incidents_router
from app.api.investigations import (
    router as investigations_router,
)
from app.api.simulator import router as simulator_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="SentinelAI",
        description=(
            "Enterprise agentic AI platform for production "
            "incident investigation and response."
        ),
        version="0.1.0",
    )

    application.include_router(
        incidents_router
    )

    application.include_router(
        simulator_router
    )

    application.include_router(
        investigations_router
    )

    return application


app = create_app()


@app.get(
    "/health",
    tags=["System"],
)
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "sentinel-ai",
        "version": "0.1.0",
    }