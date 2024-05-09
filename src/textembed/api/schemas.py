import time
from typing import Annotated, Any, Dict, List, Literal, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    id: str
    stats: Dict[str, Any]
    object: str = "model"
    owned_by: str = "textembed"
    created: int = Field(default_factory=lambda: int(time.time()))


class OpenAIModelInfo(BaseModel):
    data: List[ModelInfo]
    object: str = "list"


class EmbeddingRequest(BaseModel):
    input: List[str]
    model: Union[str, None] = None
    user: Optional[str] = None


class _EmbeddingObject(BaseModel):
    object: Literal["embedding"] = "embedding"
    embedding: list[float]
    index: int


class OpenAIEmbeddingRequest(BaseModel):
    object: Literal["embedding"] = "embedding"
    data: list[_EmbeddingObject]
    model: str
    id: str = Field(default_factory=lambda: f"textembed-{uuid4()}")
    created: int = Field(default_factory=lambda: int(time.time()))
