"""Sentence Transformers"""

from typing import Any, Dict, List

import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
from torch import Tensor

from textembed.engine.args import AsyncEngineArgs
from textembed.executor.base import BaseEmbedder


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
        self.eval()

    async def preprocess(self, sentences: List[str]) -> Any:
        """Preprocesses input sentences for embedding.

        Args:
            sentences (List[str]): List of sentences to be embedded.

        Returns:
            Any: Tokenized features ready for core processing.
        """
        features = self.tokenize(sentences)
        return features

    async def core_process(self, features: Dict[str, Tensor]) -> Tensor:
        """Runs the core embedding process on the input features.

        Args:
            features (Dict[str, Tensor]): Tokenized features.

        Returns:
            Tensor: Raw embeddings from the model.
        """
        with torch.inference_mode():
            features = util.batch_to_device(features, self.device)
            out_features = self.forward(features)["sentence_embedding"]
        return out_features

    async def postprocess(self, out_features: Tensor) -> List[np.ndarray]:
        """Postprocesses the raw embeddings to the final format.

        Args:
            out_features (Tensor): Raw embeddings from the model.

        Returns:
            np.ndarray: Postprocessed embeddings in numpy array format.
        """
        with torch.inference_mode():
            embeddings = out_features.detach().cpu().numpy()
        return embeddings

    async def generate_embeddings(self, sentences: List[str]) -> List[np.ndarray]:
        """Generates embeddings for the input sentences.

        Args:
            sentences (List[str]): Input sentences to generate embeddings for.

        Returns:
            List[np.ndarray]: Generated embeddings.
        """
        features = await self.preprocess(sentences)
        out_features = await self.core_process(features)
        embeddings = await self.postprocess(out_features)

        return embeddings
