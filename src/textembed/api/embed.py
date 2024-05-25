"""Embedding model apis"""

import asyncio
import time
from uuid import uuid4

from fastapi import APIRouter, Request, status
from fastapi.responses import ORJSONResponse

from textembed.api.schemas import (
    EmbeddingData,
    EmbeddingRequest,
    EmbeddingResponse,
    ModelDetails,
    ModelList,
)
from textembed.engine.args import AsyncEngineArgs
from textembed.engine.async_engine import AsyncEngine
from textembed.log import logger

embed_router = APIRouter(prefix="/v1", tags=["Embedding"])


@embed_router.get(
    "/models",
    response_class=ORJSONResponse,
    response_model=ModelList,
    status_code=status.HTTP_200_OK,
)
async def get_models(request: Request) -> ModelList:
    """Get the list of available embedding models.

    Args:
        request (Request): The user request.

    Returns:
        ModelList: A list of available embedding models.
    """
    engine_args: AsyncEngineArgs = request.app.state.async_engine.engine_args
    return ModelList(data=[ModelDetails(id=engine_args.model)])


@embed_router.post(
    "/embedding",
    response_class=ORJSONResponse,
    response_model=EmbeddingResponse,
    status_code=status.HTTP_200_OK,
)
async def create_embedding(
    request: Request, embed_request: EmbeddingRequest
) -> EmbeddingResponse:
    """Create embeddings for the given input text.

    Args:
        request (Request): The user request.
        embed_request (EmbeddingRequest): The request containing input text
                                        and optional model and user information.

    Returns:
        EmbeddingResponse: The response containing embedding data.
    """
    async_engine: AsyncEngine = request.app.state.async_engine

    # Ensure input
    if isinstance(embed_request.input, str):
        embed_request.input = [embed_request.input]

    start_time = time.perf_counter()

    # Generate embeddings
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    await async_engine.aembed(sentences=embed_request.input, future=future)
    embeddings = await future

    logger.info(
        "Received request with %d inputs. Processed in %.4f ms",
        len(embed_request.input),
        (time.perf_counter() - start_time) * 1000,
    )

    embedding_data = [
        EmbeddingData(
            object="embedding",
            embedding=emb,
            index=count,
        )
        for count, emb in enumerate(embeddings)
    ]

    response = EmbeddingResponse(
        object="embedding",
        data=embedding_data,
        model=async_engine.engine_args.model,
        id=f"textembed-{uuid4()}",
        created=int(time.time()),
    )

    return response
