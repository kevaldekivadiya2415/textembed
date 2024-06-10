[![Contributors](https://img.shields.io/github/contributors/kevaldekivadiya2415/textembed.svg)](https://github.com/kevaldekivadiya2415/textembed/graphs/contributors)
[![Issues](https://img.shields.io/github/issues/kevaldekivadiya2415/textembed.svg)](https://github.com/kevaldekivadiya2415/textembed/issues)
[![Apache License 2.0](https://img.shields.io/github/license/kevaldekivadiya2415/textembed.svg)](https://github.com/kevaldekivadiya2415/textembed/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/textembed)](https://pepy.tech/project/textembed)
[![Docker Pulls](https://img.shields.io/docker/pulls/kevaldekivadiya/textembed.svg)](https://hub.docker.com/r/kevaldekivadiya/textembed)
[![PyPI - Version](https://img.shields.io/pypi/v/textembed)](https://pypi.org/project/textembed/)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=kevaldekivadiya2415_textembed&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=kevaldekivadiya2415_textembed)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=kevaldekivadiya2415_textembed&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=kevaldekivadiya2415_textembed)



# TextEmbed - Embedding Inference Server

TextEmbed is a high-throughput, low-latency REST API designed for serving vector embeddings. It supports a wide range of sentence-transformer models and frameworks, making it suitable for various applications in natural language processing.

## Features

- **High Throughput & Low Latency:** Designed to handle a large number of requests efficiently.
- **Flexible Model Support:** Works with various sentence-transformer models.
- **Scalable:** Easily integrates into larger systems and scales with demand.
- **Batch Processing:** Supports batch processing for better and faster inference.
- **OpenAI Compatible REST API Endpoint:** Provides an OpenAI compatible REST API endpoint.
- **Single Line Command Deployment:** Deploy multiple models via a single command for efficient deployment.
- **Support for Embedding Formats:** Supports binary, float16, and float32 embeddings formats for faster retrieval.

## Getting Started

### Prerequisites

Ensure you have Python 3.10 or higher installed. You will also need to install the required dependencies.

### Installation

1. Install the required dependencies:
    ```bash
    pip install -U textembed
    ```

2. Start the TextEmbed server with your desired models:
    ```bash
    python3 -m textembed.server --models <Model1>, <Model2> --port <Port>
    ```

    Replace `<Model1>` and `<Model2>` with the names of the models you want to use, separated by commas. Replace `<Port>` with the port number on which you want to run the server.

For more information about the Docker deployment and configuration, please refer to the documentation [setup.md](docs/setup.md).
