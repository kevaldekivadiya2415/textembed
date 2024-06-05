# Setup Guide for TextEmbed

This document provides detailed instructions for setting up the TextEmbed server using both PyPI and Docker. Follow the steps below to get started.

## Prerequisites

Ensure you have Python 3.10 or higher installed on your machine. You will also need to install the required dependencies for the TextEmbed server.

## Installation via PyPI

1. **Install the required dependencies:**

    ```bash
    pip install -U textembed
    ```

2. **Start the TextEmbed server with your desired models:**

    ```bash
    python3 -m textembed.server --models <Model1>, <Model2> --port <Port>
    ```

3. **For more information and additional options, run:**

    ```bash
    python3 -m textembed.server --help
    ```
    - --models: `<Model1>`, `<Model2>`: Comma-separated list of Huggingface models to be used.
    - --served_model_names: `<Name1>`, `<Name2>`: Comma-separated list of names under which the models will be served.
    - --host: `<Host>`: The host address on which the application will run.
    - --port: `<Port>`: The port number on which the application will run.
    - --workers: `<NumberOfWorkers>`: The number of worker processes for batch processing.
    - --batch_size: `<BatchSize>`: The batch size for processing requests.
    - --embedding_dtype: `<EmbeddingDtype>`: The data type for the embeddings. Choose from 'binary', 'float16', or 'float32'.

## Running with Docker (Recommended)

You can also run TextEmbed using Docker. The Docker image is available on Docker Hub.

1. **Pull the Docker image:**

    ```bash
    docker pull kevaldekivadiya/textembed:latest
    ```

2. **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 kevaldekivadiya/textembed:latest --models <Model1>, <Model2> <Host> --port <Port>
    ```

3. **For more information and additional options, run:**

    ```bash
    docker run kevaldekivadiya/textembed:latest --help
    ```

This command will display the help message for the TextEmbed server, detailing the available options and usage instructions.

## Accessing the API
Once the server is running, you can access the API documentation via Swagger UI by navigating to `http://localhost:8000/docs` in your web browser.

