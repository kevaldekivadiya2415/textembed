"""Embedding model apis"""

import asyncio
import time
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import ORJSONResponse

from textembed.api.dependencies import valid_token_dependency
from textembed.api.errors import ModelNotFoundException
from textembed.api.schemas import (
    EmbeddingData,
    EmbeddingRequest,
    EmbeddingResponse,
    ModelDetails,
    ModelList,
    Usage,
)
from textembed.engine.args import AsyncEngineArgs
from textembed.engine.async_engine import AsyncEngine
from textembed.engine.async_engine_array import AsyncEngineArray
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
    async_engine_args_list: List[AsyncEngineArgs] = (
        request.app.state.async_engine_array.engine_args
    )
    return ModelList(
        data=[
            ModelDetails(
                id=engine_args.model,
                served_model_name=engine_args.served_model_name,  # type: ignore
            )
            for engine_args in async_engine_args_list
        ]
    )


@embed_router.post(
    "/embedding",
    response_class=ORJSONResponse,
    response_model=EmbeddingResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(valid_token_dependency)],  # type: ignore
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

    # Directly retrieve the AsyncEngineArgs from AsyncEngineArray
    async_engine_array: AsyncEngineArray = request.app.state.async_engine_array
    async_engine_args_list: List[AsyncEngineArgs] = async_engine_array.engine_args

    # Check if the requested model is in the engine arguments
    if embed_request.model not in [
        engine_args.model for engine_args in async_engine_args_list
    ]:
        raise ModelNotFoundException(
            message=f"The requested model `{embed_request.model}` was not found. "
            f"Please ensure that you have specified the correct model name. "
            f"Currently served models `{[engine_args.model for engine_args in async_engine_args_list]}`."
        )

    # Get engine for the requested model
    engine: AsyncEngine = async_engine_array[embed_request.model]  # type: ignore

    # Ensure input
    if isinstance(embed_request.input, str):
        embed_request.input = [embed_request.input]

    start_time = time.perf_counter()

    # Generate embeddings
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    await engine.aembed(sentences=embed_request.input, future=future)  # type: ignore
    results = await future

    logger.info(
        "Received request with %d inputs. Processed in %.4f ms",
        len(embed_request.input),
        (time.perf_counter() - start_time) * 1000,
    )

    embeddings = results[0]
    usage = results[1]
    embedding_data = [
        EmbeddingData(
            object="embedding",
            embedding=emb,
            index=count,
            usage=Usage(
                prompt_tokens=usage[count],
                total_tokens=usage[count],
            ),
        )
        for count, emb in enumerate(embeddings)
    ]

    response = EmbeddingResponse(
        object="embedding",
        data=embedding_data,
        model=embed_request.model,
        id=f"textembed-{uuid4()}",
        created=int(time.time()),
    )

    return response
