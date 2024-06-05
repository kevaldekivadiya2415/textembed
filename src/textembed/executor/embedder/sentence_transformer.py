"""Sentence Transformers"""

from typing import Dict, List, Tuple

import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
from torch import Tensor

from textembed.engine.args import AsyncEngineArgs
from textembed.executor.base import BaseEmbedder
from textembed.executor.primitives import EmbeddingDtype


class SentenceTransformerEmbedder(SentenceTransformer, BaseEmbedder):
    """Sentence Transformer Embedder for embedding creation.

    This class extends SentenceTransformer and implements the BaseEmbedder interface
    to provide a complete embedding creation workflow including preprocessing,
    core processing, and postprocessing steps.
    """

    def __init__(self, engine_args: AsyncEngineArgs) -> None:
        """Initializes the embedder with the given engine arguments.

        Args:
            engine_args (AsyncEngineArgs): The arguments required to configure the engine.
        """
        super().__init__(
            model_name_or_path=engine_args.model,
            device="cpu",
            trust_remote_code=engine_args.trust_remote_code,
        )
        self.embedding_dtype = engine_args.embedding_dtype
        self.engine_args = engine_args
        self.eval()

    async def warm_up(self) -> None:
        """Warm up the model by performing a dummy inference."""
        sample_sentences = ["This is a sample sentence."] * 10
        # Perform inference
        await self.process_batch(sample_sentences)

    async def preprocess(
        self, sentences: List[str]
    ) -> Tuple[Dict[str, Tensor], List[int]]:
        """Tokenizes the input sentences.

        Args:
            sentences (List[str]): List of sentences to be tokenized.

        Returns:
            Tuple[Dict[str, Tensor], List[int]]: Tokenized features and lengths of sentences
        """
        tokenized = self.tokenize(sentences)
        usage = [len(sentence) for sentence in sentences]
        return tokenized, usage

    async def transfer_to_device(
        self, features: Dict[str, Tensor]
    ) -> Dict[str, Tensor]:
        """Moves the tokenized features to the appropriate device.

        Args:
            features (Dict[str, Tensor]): Tokenized features.

        Returns:
            Dict[str, Tensor]: Features moved to the specified device.
        """
        return util.batch_to_device(features, self.device)

    async def generate_embeddings(self, features: Dict[str, Tensor]) -> Tensor:
        """Performs the forward pass to generate sentence embeddings.

        Args:
            features (Dict[str, Tensor]): Tokenized features moved to the device.

        Returns:
            Tensor: Raw embeddings from the model.
        """
        with torch.inference_mode():
            return self.forward(features)["sentence_embedding"]

    async def postprocess(self, out_features: Tensor) -> np.ndarray:
        """Converts the output tensors to numpy arrays of the specified data type.

        Args:
            out_features (Tensor): Raw embeddings from the model.

        Returns:
            np.ndarray: Postprocessed embeddings in the specified numpy array format.
        """
        embeddings: np.ndarray = out_features.detach().cpu().numpy()
        if self.embedding_dtype == EmbeddingDtype.BINARY.value:
            return (embeddings > 0).astype(np.uint8)
        elif self.embedding_dtype == EmbeddingDtype.FLOAT16.value:
            return embeddings.astype(np.float16)
        elif self.embedding_dtype == EmbeddingDtype.FLOAT32.value:
            return embeddings.astype(np.float32)
        else:
            raise ValueError(f"Unsupported dtype: {self.embedding_dtype}")

    async def process_batch(self, sentences: List[str]) -> Tuple[np.ndarray, List[int]]:
        """Processes a batch of sentences to generate embeddings.

        Args:
            sentences (List[str]): List of sentences to be embedded.

        Returns:
            Tuple[np.ndarray, List[int]]: Generated embeddings and lengths of sentences.
        """
        features, lengths = await self.preprocess(sentences)
        features = await self.transfer_to_device(features)
        out_features = await self.generate_embeddings(features)
        embeddings = await self.postprocess(out_features)
        return embeddings, lengths  # type: ignore
