"""To start the application using CLI."""

import typer
import uvicorn
from typing_extensions import Annotated

from textembed.application.application import create_application
from textembed.engine.args import AsyncEngineArgs

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
):
    """
    Starts the application with the specified configuration.

    Args:
        model (str): The name or path of the Huggingface model to be used.
        served_model_name (str): The name under which the model will be served.
        trust_remote_code (bool): Whether to trust remote code when loading the model.
        host (str): The host address on which the application will run.
        port (int): The port number on which the application will run.
    """
    engine_args = AsyncEngineArgs(
        model=model,
        served_model_name=served_model_name,
        trust_remote_code=trust_remote_code,
    )

    app = create_application(
        engine_args=engine_args,
        doc_extra={"host": host, "port": port},
    )
    uvicorn.run(app, host=host, port=port, log_level="critical")


if __name__ == "__main__":
    app_typer()