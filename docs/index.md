# TextEmbed

**TextEmbed** is a high-throughput, low-latency REST API for serving vector embeddings. It supports a wide range of sentence-transformer models and frameworks. Developed under the Apache-2.0 License, TextEmbed is designed for flexibility and scalability in embedding applications.

## Key Features

- **Flexible Model Support**: Deploy any model from supported sentence-transformer frameworks, including SentenceTransformers.
- **High-Performance Inference**: Utilizes efficient backends like torch, ONNX, TensorRT, and FlashAttention for optimal performance across various devices.
- **Dynamic Batching**: Processes new embedding requests as soon as resources are available, ensuring high throughput.
- **Accurate and Tested**: Provides embeddings consistent with SentenceTransformers, with unit and end-to-end testing for reliability.
- **User-Friendly API**: Built with FastAPI and fully documented via Swagger, aligning with OpenAI's Embedding specs.

## Getting Started

### Installation via PyPI

1. **Install TextEmbed:**

    ```bash
    pip install -U textembed
    ```

2. **Start the Server:**

    ```bash
    python3 -m textembed.server --models <Model1>,<Model2> --port <Port>
    ```

3. **View Help Options:**

    ```bash
    python3 -m textembed.server --help
    ```

### Running with Docker (Recommended)

1. **Pull the Docker Image:**

    ```bash
    docker pull kevaldekivadiya/textembed:latest
    ```

2. **Run the Docker Container:**

    ```bash
    docker run -it --gpus all \
     -v $PWD/data:/app/.cache \
     -p 8000:8000 \
     kevaldekivadiya/textembed:latest \
     --models <Model1>,<Model2> \
     --port 8000
    ```

3. **View Help Options:**

    ```bash
    docker run kevaldekivadiya/textembed:latest --help
    ```

## Accessing the API

Access the API documentation via Swagger UI at `http://localhost:8000/docs`.
