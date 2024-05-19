"""Base class for embeddings creation"""

from abc import ABC, abstractmethod
from typing import Any, List


class BaseEmbedder(ABC):
    """Abstract base class for transformer models.

    This class outlines the required methods and properties for a transformer model.
    It includes methods for preprocessing, core processing, postprocessing, and generating embeddings.
    """

    @abstractmethod
    async def preprocess(self, sentences: List[str]) -> Any:
        """Preprocesses input sentences for tokenization and feature preparation.

        Args:
            sentences (List[str]): List of sentences to be tokenized and prepared.

        Returns:
            Any: Preprocessed data ready for the core encoding step.
        """

    @abstractmethod
    async def core_process(self, features: Any) -> Any:
        """Runs the core processing step for the model, performing inference.

        Args:
            features (Any): The features prepared by the preprocessing step.

        Returns:
            Any: The output features from the model process.
        """

    @abstractmethod
    async def postprocess(self, out_features: Any) -> Any:
        """Postprocesses the output features from the inference step.

        Args:
            out_features (Any): The raw output features from the model.

        Returns:
            Any: Postprocessed data, typically converted to a desired format.
        """

    @abstractmethod
    async def generate_embeddings(self, sentences: List[str]) -> Any:
        """Generates embeddings for the input sentences.

        Args:
            sentences (Any): Input sentences to generate embeddings for.

        Returns:
            Any: Generated embeddings.
        """
