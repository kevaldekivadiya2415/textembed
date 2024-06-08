"""Application configuration"""

from contextlib import asynccontextmanager
from typing import List, Union

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

import textembed
from textembed.api import docs
from textembed.api.embed import embed_router
from textembed.api.monitor import monitor_router
from textembed.engine.args import AsyncEngineArgs
from textembed.engine.async_engine_array import AsyncEngineArray
from textembed.log import logger


def create_application(
    engine_args_list: List[AsyncEngineArgs],
    doc_extra: dict,
    api_key: Union[str, None] = None,
) -> FastAPI:
    """Crate FastAPI Application

    Args:
        engine_args (AsyncEngineArgs): Async engine arguments
        doc_extra (dict): Dict of host and port.
        api_key (Union(str, None)): Api key.

    Returns:
        FastAPI: FastAPI application
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Context manager for FastAPI app lifespan.
        """
        logger.info(
            docs.startup_message(
                host=doc_extra.get("host", "localhost"),
                port=doc_extra.get("port", 8000),
            )
        )
        app.state.async_engine_array = AsyncEngineArray.from_args(
            engine_args_list=engine_args_list
        )
        app.state.api_key = api_key

        await app.state.async_engine_array.start_all()
        yield
        await app.state.async_engine_array.stop_all()

    app = FastAPI(
        title=docs.FASTAPI_TITLE,
        summary=docs.FASTAPI_SUMMARY,
        description=docs.FASTAPI_DESCRIPTION,
        lifespan=lifespan,
        version=textembed.__version__,
        contact={"name": "Keval Dekivadiya"},
        docs_url="/docs",
        license_info={"name": "Apache License 2", "identifier": "Apache"},
    )

    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=[".*admin.*"],
        inprogress_name="inprogress",
        inprogress_labels=True,
    )
    instrumentator.instrument(app)

    app.include_router(monitor_router)
    app.include_router(embed_router)

    return app
