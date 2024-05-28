"""Base class for embeddings creation"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

import numpy as np
from torch import Tensor


class BaseEmbedder(ABC):
    """Abstract base class for embedding models.

    This class outlines the required methods and properties for an embedding model.
    It includes methods for preprocessing, core processing, postprocessing, and generating embeddings.
    """

    @abstractmethod
    async def preprocess(
        self, sentences: List[str]
    ) -> Tuple[Dict[str, Tensor], List[int]]:
        """Tokenize the input sentences.

        Args:
            sentences (List[str]): List of sentences to be tokenized.

        Returns:
            Tuple[Dict[str, Tensor], List[int]]: Tokenized features and lengths of sentences
        """

    @abstractmethod
    async def transfer_to_device(
        self, features: Dict[str, Tensor]
    ) -> Dict[str, Tensor]:
        """Moves the tokenized features to the appropriate device.

        Args:
            features (Dict[str, Tensor]): Tokenized features.

        Returns:
            Dict[str, Tensor]: Features moved to the specified device.
        """

    @abstractmethod
    async def generate_embeddings(self, features: Dict[str, Tensor]) -> Tensor:
        """Performs the forward pass to generate sentence embeddings.

        Args:
            features (Dict[str, Tensor]): Tokenized features moved to the device.

        Returns:
            Tensor: Raw embeddings from the model.
        """

    @abstractmethod
    async def postprocess(self, out_features: Tensor) -> np.ndarray:
        """Converts the output tensors to numpy arrays.

        Args:
            out_features (Tensor): Raw embeddings from the model.

        Returns:
            np.ndarray: Postprocessed embeddings in numpy array format.
        """

    @abstractmethod
    async def process_batch(self, sentences: List[str]) -> Tuple[np.ndarray, List[int]]:
        """Processes a batch of sentences to generate embeddings.

        Args:
            sentences (List[str]): List of sentences to be embedded.

        Returns:
            Tuple[np.ndarray, List[int]]: Generated embeddings and lengths of sentences.
        """
