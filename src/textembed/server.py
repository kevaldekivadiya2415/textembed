"""To start the application using CLI."""

import multiprocessing
import warnings
from typing import Union

import typer
import uvicorn
from typing_extensions import Annotated

from textembed.api.errors import HandleExceptions
from textembed.application.application import create_application
from textembed.engine.args import AsyncEngineArgs

# Filter out all warnings
warnings.filterwarnings("ignore")

# Initialize Typer app
app_typer = typer.Typer()


@app_typer.command()
def start_application(
    models: Annotated[
        str,
        typer.Option(help="Comma-separated list of Huggingface models to be used."),
    ] = "sentence-transformers/all-MiniLM-L6-v2, sentence-transformers/all-MiniLM-L12-v2",
    served_model_names: Annotated[
        Union[str, None],
        typer.Option(
            help="Comma-separated list of names under which the models will be served."
        ),
    ] = None,
    trust_remote_code: Annotated[
        bool,
        typer.Option(help="Whether to trust remote code when loading the models."),
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
            help="The data type for the embeddings. Choose from 'binary', 'float16', or 'float32'. Default is 'float32'."
        ),
    ] = "float32",
    api_key: Annotated[
        Union[str, None],
        typer.Option(
            help="Your API key for authentication. Make sure to keep it secure. Do not share it with others."
        ),
    ] = None,
):
    """
    Starts the application with the specified configuration.

    Args:
        models (str): Comma-separated list of Huggingface models to be used.
        served_model_names (str): Comma-separated list of names under which the models will be served.
        trust_remote_code (bool): Whether to trust remote code when loading the models.
        host (str): The host address on which the application will run.
        port (int): The port number on which the application will run.
        workers (int): The number of worker processes.
        batch_size (int): The batch size for processing requests.
        embedding_dtype (str): The data type for the embeddings. Choose from 'binary', 'float16', or 'float32'.
        api_key Union[str, None]: Your API key for authentication. Make sure to keep it secure. Do not share it with others.
    """

    # Split the models and served model names
    models_list = models.split(",")
    if served_model_names is None:
        served_model_names_list = models_list
    else:
        served_model_names_list = served_model_names.split(",")

    if len(models_list) != len(served_model_names_list):
        raise ValueError(
            "The number of models must match the number of served model names."
        )

    # Create a list of AsyncEngineArgs instances
    engine_args_list = []
    for idx, model in enumerate(models_list):
        engine_args = AsyncEngineArgs(
            model=model.strip(),
            served_model_name=served_model_names_list[idx].strip(),
            trust_remote_code=trust_remote_code,
            workers=workers if workers is not None else multiprocessing.cpu_count(),
            batch_size=batch_size,
            embedding_dtype=embedding_dtype,
        )
        engine_args_list.append(engine_args)

    # Create the application
    app = create_application(
        engine_args_list=engine_args_list,
        doc_extra={"host": host, "port": port},
        api_key=api_key,
    )

    # Handle Errors
    HandleExceptions(app=app)

    # Run the application
    uvicorn.run(app, host=host, port=port, log_level="error")


if __name__ == "__main__":
    app_typer()
