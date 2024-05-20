# TextEmbed - Embedding Inference Server

TextEmbed is a high-throughput, low-latency REST API designed for serving vector embeddings. It supports a wide range of sentence-transformer models and frameworks, making it suitable for various applications in natural language processing.

## Features

- **High Throughput & Low Latency:** Designed to handle a large number of requests efficiently.
- **Flexible Model Support:** Works with various sentence-transformer models.
- **Scalable:** Easily integrates into larger systems and scales with demand.
- **REST API:** Simple and accessible API endpoints.

## Getting Started

### Prerequisites

Ensure you have Python 3.10 or higher installed. You will also need to install the required dependencies.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/kevaldekivadiya2415/textembed.git
    cd textembed
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

1. Set up the package in development mode:
    ```bash
    python3 setup.py develop
    ```

2. Start the TextEmbed server with your desired model:
    ```bash
    python3 -m textembed.server --model <Model Name>
    ```

    Replace `<Model Name>` with the name of the model you want to use.

3. For more information and additional options, run:
    ```bash
    python3 -m textembed.server --help
    ```

### Accessing the API

Once the server is running, you can access the API documentation via Swagger UI at:

