"""Application configuration"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

import textembed
from textembed.api import docs
from textembed.api.embed import embed_router
from textembed.api.monitor import monitor_router
from textembed.engine.args import AsyncEngineArgs
from textembed.engine.async_engine import AsyncEngine
from textembed.log import logger


def create_application(
    engine_args: AsyncEngineArgs,
    doc_extra: dict,
) -> FastAPI:
    """_summary_

    Args:
        engine_args (AsyncEngineArgs): Async engine arguments
        doc_extra (dict): Dict of host and port.

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
        app.state.engine = AsyncEngine.from_args(engine_args=engine_args)
        await app.state.engine.start()
        yield
        await app.state.engine.stop()

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
