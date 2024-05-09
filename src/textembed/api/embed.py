import time
import asyncio

from fastapi import APIRouter, Request, status
from fastapi.responses import ORJSONResponse

from textembed.api.schemas import (
    EmbeddingRequest,
    ModelInfo,
    OpenAIModelInfo,
    OpenAIEmbeddingRequest,
)
from textembed.engine.async_engine import AsyncEngine
from textembed.log import logger

embed_router = APIRouter(prefix="/v1", tags=["Embedding"])


@embed_router.get(
    "/models",
    response_class=ORJSONResponse,
    response_model=OpenAIModelInfo,
    status_code=status.HTTP_200_OK,
)
async def _get_model(request: Request):
    try:
        engine: AsyncEngine = request.app.state.engine.engine_args
        return OpenAIModelInfo(
            data=[ModelInfo(id=engine.served_model_name, stats={"cpu": "2"})]
        )
    except Exception as exc:
        logger.exception(exc)


@embed_router.post(
    "/embedding",
    response_class=ORJSONResponse,
    response_model=OpenAIEmbeddingRequest,
    status_code=status.HTTP_200_OK,
)
async def _embedding(request: Request, embed_request: EmbeddingRequest):
    try:
        engine: AsyncEngine = request.app.state.engine
        # check string
        if isinstance(embed_request.input, str):
            embed_request.input = [embed_request.input]

        logger.debug("[📝] Received request with %s inputs ", len(embed_request.input))
        start = time.perf_counter()

        embeddings = await engine.aembed(sentences=embed_request.input)

        duration = (time.perf_counter() - start) * 1000
        logger.debug("[✅] Done in %s ms", duration)

        return OpenAIEmbeddingRequest(
            data=[
                dict(
                    object="embedding",
                    embedding=emb,
                    index=count,
                )
                for count, emb in enumerate(embeddings)
            ],
            model=engine.engine_args.served_model_name,
        )

    except Exception as exc:
        logger.exception(exc)
