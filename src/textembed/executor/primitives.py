"""Primitives"""

from enum import Enum
from typing import Literal

ModelCapabilities = Literal["embedding"]


class EmbeddingDtype(Enum):
    """
    Enum representing the different data types that can be used for embeddings.

    Attributes:
        FLOAT32 (str): Represents 32-bit floating point embeddings.
        INT8 (str): Represents 8-bit integer embeddings.
        BINARY (str): Represents binary embeddings.
    """

    FLOAT32 = "float32"
    INT8 = "int8"
    BINARY = "binary"
