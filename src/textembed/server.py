"""To start the application using CLI."""

import multiprocessing
import warnings

import typer
import uvicorn
from typing_extensions import Annotated

from textembed.api.errors import HandleExceptions
from textembed.application.application import create_application
from textembed.engine.args import AsyncEngineArgs

# Filter out all warnings
warnings.filterwarnings("ignore")

app_typer = typer.Typer()


@app_typer.command()
def start_application(
    model: Annotated[
        str,
        typer.Option(help="The name or path of the Huggingface model to be used."),
    ] = "sentence-transformers/all-MiniLM-L6-v2",
    served_model_name: Annotated[
        str,
        typer.Option(help="The name under which the model will be served."),
    ] = "",
    trust_remote_code: Annotated[
        bool,
        typer.Option(help="Whether to trust remote code when loading the model."),
    ] = True,
    host: Annotated[
        str,
        typer.Option(help="The host address on which the application will run."),
    ] = "0.0.0.0",
    port: Annotated[
        int,
        typer.Option(help="The port number on which the application will run."),
    ] = 8000,
    workers: Annotated[
        int,
        typer.Option(help="The number of worker processes."),
    ] = None,  # type: ignore
    batch_size: Annotated[
        int,
        typer.Option(help="The batch size for processing requests."),
    ] = 32,
    embedding_dtype: Annotated[
        str,
        typer.Option(
            help="The data type for the embeddings. Choose from 'binary', 'int8', 'float16', or 'float32'. Default is 'float32'."
        ),
    ] = "float32",
):
    """
    Starts the application with the specified configuration.

    Args:
        model (str): The name or path of the Huggingface model to be used.
        served_model_name (str): The name under which the model will be served.
        trust_remote_code (bool): Whether to trust remote code when loading the model.
        host (str): The host address on which the application will run.
        port (int): The port number on which the application will run.
        workers (int): The number of worker processes.
        batch_size (int): The batch size for processing requests.
        embedding_dtype (str): The data type for the embeddings. Choose from 'binary', 'int8', 'float16', or 'float32
    """
    engine_args = AsyncEngineArgs(
        model=model,
        served_model_name=served_model_name or None,  # Set to None if empty string
        trust_remote_code=trust_remote_code,
        workers=workers if workers is not None else multiprocessing.cpu_count(),
        batch_size=batch_size,
        embedding_dtype=embedding_dtype,
    )

    app = create_application(
        engine_args=engine_args,
        doc_extra={"host": host, "port": port},
    )

    # Handle Errors
    HandleExceptions(app=app)

    uvicorn.run(app, host=host, port=port, log_level="error")


if __name__ == "__main__":
    app_typer()
