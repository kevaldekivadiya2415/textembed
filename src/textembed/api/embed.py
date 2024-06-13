"""Embedding model apis"""

import asyncio
import base64
import time
from io import BytesIO
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import ORJSONResponse
from PIL import Image

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


async def get_engine(request: Request, embed_request: EmbeddingRequest):
    """Retrieve the appropriate engine for the requested model.
    Args:
        request (Request): The HTTP request object containing the application state.
        embed_request (EmbeddingRequest): The request object containing details
                                          about the embedding, including the model name.

    Raises:
        ModelNotFoundException: If the specified model is not found in the available engines.

    Returns:
        AsyncEngine: The engine corresponding to the requested model.
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

    return engine


async def prepare_response(results: list, embed_request: EmbeddingRequest):
    """
    Prepare the response for the embedding request.

    Args:
        results (list): A list containing the embeddings and their usage information.
            - results[0] (list): A list of embeddings.
            - results[1] (list): A list of usage data corresponding to each embedding.
        embed_request (EmbeddingRequest): The request object containing details about the embedding, 
                                          including the model name.

    Returns:
        EmbeddingResponse: The structured response containing the embeddings, usage data, 
                           and other metadata.
    """
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
    # Get engine for the requested model
    engine: AsyncEngine = await get_engine(request=request, embed_request=embed_request)

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

    return await prepare_response(results=results, embed_request=embed_request)


@embed_router.post(
    "/image_embedding",
    response_class=ORJSONResponse,
    response_model=EmbeddingResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(valid_token_dependency)],  # type: ignore
)
async def create_image_embedding(
    request: Request, embed_request: EmbeddingRequest
) -> EmbeddingResponse:
    """Create embeddings for the given input base64 image.

    Args:
        request (Request): The user request.
        embed_request (EmbeddingRequest): The request containing input base64 image
                                        and optional model and user information.

    Returns:
        EmbeddingResponse: The response containing embedding data.
    """
    # Get engine for the requested model
    engine: AsyncEngine = await get_engine(request=request, embed_request=embed_request)

    # Ensure input
    if isinstance(embed_request.input, str):
        embed_request.input = [embed_request.input]

    start_time = time.perf_counter()

    image_input = [
        Image.open(BytesIO(base64.b64decode(image))).convert("RGB")
        for image in embed_request.input
    ]

    # Generate embeddings
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    await engine.aembed(sentences=image_input, future=future)  # type: ignore
    results = await future

    logger.info(
        "Received request with %d inputs. Processed in %.4f ms",
        len(embed_request.input),
        (time.perf_counter() - start_time) * 1000,
    )

    return await prepare_response(results=results, embed_request=embed_request)
