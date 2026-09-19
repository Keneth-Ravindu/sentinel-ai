from fastapi import FastAPI


def create_app() -> FastAPI:
    application = FastAPI(
        title="SentinelAI",
        description=(
            "Enterprise agentic AI platform for production "
            "incident investigation and response."
        ),
        version="0.1.0",
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