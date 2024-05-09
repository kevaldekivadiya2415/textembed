from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import FastAPI

import textembed
from textembed.api import docs, errors
from textembed.engine.args import AsyncEngineArgs
from textembed.engine.async_engine import AsyncEngine
from textembed.log import logger


def create_server(
    engine_args: AsyncEngineArgs,
    doc_extra: dict = {},
) -> FastAPI:
    """
    Create and configure a FastAPI app.
    """

    from textembed.api.monitor import monitor_router
    from textembed.api.embed import embed_router

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

    app.add_exception_handler(errors.OpenAIException, errors.openai_exception_handler)

    app.include_router(monitor_router)
    app.include_router(embed_router)

    return app


def _start_app(
    model: str = "hello",
    served_model_name: Optional[str] = "hello",
    batch_size: int = 16,
    host: str = "0.0.0.0",
    port: int = 8000,
):
    engine_args = AsyncEngineArgs(
        model=model,
        served_model_name=served_model_name,
        batch_size=batch_size,
    )

    app = create_server(
        engine_args=engine_args,
        doc_extra=dict(host=host, port=port),
    )
    uvicorn.run(app, host=host, port=port)


def cli():
    """Fires the command line using Python `typer.run()`"""
    import typer

    typer.run(_start_app)


if __name__ == "__main__":
    cli()
