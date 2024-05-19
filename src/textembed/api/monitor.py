"""Monitor FastAPI app."""

import time

from fastapi import APIRouter, Response
from prometheus_client import REGISTRY, generate_latest

from textembed.api.schemas import HealthCheck, Root

monitor_router = APIRouter(tags=["Monitor"])


@monitor_router.get("/")
async def _root() -> Root:
    """
    Root endpoint.

    This endpoint returns a basic response indicating that the
    TextEmbed service is running.

    Returns:
        Root: An object containing a message indicating service status.
    """
    return Root(
        payload=None,
        message="TextEmbed service.",
        code=200,
    )


@monitor_router.get("/health")
async def _health() -> HealthCheck:
    """
    Health check endpoint.

    This endpoint returns a health check response indicating the
    current status of the server with a Unix timestamp.

    Returns:
        HealthCheck: An object containing the Unix timestamp and a message.
    """
    return HealthCheck(
        payload={"unix": int(time.time())},
        message="Health check done",
        code=200,
    )


@monitor_router.get("/metrics")
async def metrics() -> Response:
    """
    Endpoint to retrieve the current metrics.

    This endpoint generates and returns the latest metrics collected by the
    Prometheus REGISTRY. The metrics are returned in a plain text format
    that is compatible with Prometheus scraping.

    Returns:
        Response: A response object containing the latest metrics in plain text format.
    """
    metrics_str = generate_latest(REGISTRY)
    return Response(content=metrics_str, media_type="text/plain")
