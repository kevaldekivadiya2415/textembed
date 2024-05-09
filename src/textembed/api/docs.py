from __future__ import annotations

import textembed

FASTAPI_TITLE = "TextEmbed - Embedding Inference Server"
FASTAPI_SUMMARY = (
    "TextEmbed is a high-throughput, low-latency REST API "
    "for serving vector embeddings, supporting a wide "
    "range of sentence-transformer models and frameworks."
)
FASTAPI_DESCRIPTION = ""


def startup_message(host: str, port: str) -> str:

    return f"""

TextEmbed - Embedding Inference Server
Apache License 2: Copyright (c) 2024 Keval Dekivadiya
Version {textembed.__version__}

Open the Docs via Swagger UI:
http://{host}:{port}/docs
"""
