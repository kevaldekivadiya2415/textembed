"""Pydantic models"""

import time
from typing import List, Literal, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    """Health check response model.

    Attributes:
        payload (Optional[Union[str, int, float, dict, list]], optional): Payload data of any type.
        message (Optional[str], optional): Message associated with the health check.
        code (Optional[int], optional): Status code for the health check.
    """

    payload: Optional[Union[str, int, float, dict, list]] = None
    message: Optional[str] = None
    code: Optional[int] = None


class Root(BaseModel):
    """Root response model.

    Attributes:
        payload (Optional[Union[str, int, float, dict, list]], optional): Payload data of any type.
        message (Optional[str], optional): Message associated with the root response.
        code (Optional[int], optional): Status code for the root response.
    """

    payload: Optional[Union[str, int, float, dict, list]] = None
    message: Optional[str] = None
    code: Optional[int] = None


class ModelDetails(BaseModel):
    """Details of a model.

    Attributes:
        id (str): Model name or id.
        served_model_name (str): Served model name, default is "".
        object (str): Type of the object, default is "model".
        owned_by (str): Owner of the model, default is "textembed".
        created (int): Timestamp when the model details were created.
    """

    id: str
    served_model_name: str
    object: str = "model"
    owned_by: str = "textembed"
    created: int = Field(default_factory=lambda: int(time.time()))


class ModelList(BaseModel):
    """List of model details objects.

    Attributes:
        data (List[ModelDetails]): List of model details objects.
        object (str): Type of the object, default is "list".
    """

    data: List[ModelDetails]
    object: str = "list"


class EmbeddingRequest(BaseModel):
    """Request for embedding text data.

    Attributes:
        input (List[str]): List of input sentences to be embedded.
        model str: Model to be used for embedding.
        user (Optional[str], optional): User making the request.
    """

    input: List[str]
    model: str
    user: Optional[str] = None


class Usage(BaseModel):
    """Sentence prompt and total tokens

    Attributes:
        prompt_tokens (str): Count of prompt tokens.
        total_tokens (str): Count of total tokens.
    """

    prompt_tokens: int
    total_tokens: int


class EmbeddingData(BaseModel):
    """Embedding data containing the embedding vector and index.

    Attributes:
        object (Literal["embedding"]): Type of the object, default is "embedding".
        embedding (List[Union[float, int]]): Embedding vector.
        index (int): Index of the embedding in the input list.
    """

    object: Literal["embedding"] = "embedding"
    embedding: List[Union[float, int]]
    usage: Usage
    index: int


class EmbeddingResponse(BaseModel):
    """Response containing embedding data in OpenAI format.

    Attributes:
        object (Literal["embedding"]): Type of the object, default is "embedding".
        data (List[EmbeddingData]): List of embedding data objects.
        model (str): Model used for generating embeddings.
        id (str): Unique identifier for the request, default is a UUID4 string prefixed with "textembed".
        created (int): Timestamp when the request was created.
    """

    object: Literal["embedding"] = "embedding"
    data: List[EmbeddingData]
    model: str
    id: str = Field(default_factory=lambda: f"textembed-{uuid4()}")
    created: int = Field(default_factory=lambda: int(time.time()))
