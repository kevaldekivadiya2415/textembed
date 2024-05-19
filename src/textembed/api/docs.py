"""FastAPI title, summary and description."""

from __future__ import annotations

import textembed

FASTAPI_TITLE = "TextEmbed - Embedding Inference Server"
FASTAPI_SUMMARY = (
    "TextEmbed is a REST API designed for high-throughput and low-latency vector embedding "
    "services. It supports a wide array of sentence-transformer models and frameworks, "
    "making it suitable for diverse applications in natural language processing."
)
FASTAPI_DESCRIPTION = (
    "TextEmbed provides a robust and scalable REST API for generating vector embeddings from text. "
    "Built for performance and flexibility, it supports various sentence-transformer models, allowing "
    "users to easily integrate state-of-the-art NLP techniques into their applications. Whether you need "
    "embeddings for search, recommendation, or other NLP tasks, TextEmbed delivers with high efficiency."
)


def startup_message(host: str, port: str) -> str:
    """
    Generate a startup message with information about the TextEmbed server.

    Args:
        host (str): The host address where the server is running.
        port (str): The port number on which the server is listening.

    Returns:
        str: A formatted startup message with server details and documentation link.
    """
    return f"""
TextEmbed - Embedding Inference Server
Apache License 2: Copyright (c) 2024 Keval Dekivadiya
Version {textembed.__version__}

Open the Docs via Swagger UI:
http://{host}:{port}/docs
"""
