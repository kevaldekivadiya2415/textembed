"""Primitives"""

from enum import Enum
from typing import Literal

ModelCapabilities = Literal["embedding"]


class EmbeddingDtype(Enum):
    """
    Enum representing the different data types that can be used for embeddings.

    Attributes:
        FLOAT32 (str): Represents 32-bit floating point embeddings.
        FLOAT16 (str): Represents 16-bit floating point embeddings.
        BINARY (str): Represents binary embeddings.
    """

    FLOAT32 = "float32"
    FLOAT16 = "float16"
    BINARY = "binary"
