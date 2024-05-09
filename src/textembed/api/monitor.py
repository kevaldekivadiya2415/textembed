from fastapi import APIRouter
import time
from .response import HealthCheck, Root

monitor_router = APIRouter()


@monitor_router.get("/health")
async def _health() -> HealthCheck:
    """
    Health check endpoint

    Returns:
        HealthCheck: Health check response object
    """
    return HealthCheck(
        payload={"unix": int(time.time())},  # Unix timestamp
        message="Health check done",
        code=200,
    )


@monitor_router.get("/")
async def _root() -> Root:
    """
    Root endpoint

    Returns:
        Root: Root response object
    """
    return Root(
        payload=None,  # No payload for root endpoint
        message="Text embed service.",
        code=200,
    )
