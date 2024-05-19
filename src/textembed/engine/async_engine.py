"""Asynchronous engine creation."""

from typing import List

import numpy as np

from textembed.engine.args import AsyncEngineArgs
from textembed.executor.embedder.sentence_transformer import SentenceTransformerEmbedder
from textembed.log import logger


class AsyncEngine:
    """Asynchronous engine for embedding text data.

    This class provides functionality to asynchronously handle and process
    text data using an underlying engine defined by `AsyncEngineArgs`.

    Attributes:
        engine_args (AsyncEngineArgs): Arguments required to initialize the engine.
        running (bool): Flag indicating if the engine is currently running.
    """

    def __init__(self, engine_args: AsyncEngineArgs) -> None:
        """
        Initialize the asynchronous engine.

        Args:
            engine_args (AsyncEngineArgs): Arguments required to initialize the engine.
        """
        self._engine_args = engine_args
        self.running = False
        self.model = None

    @classmethod
    def from_args(cls, engine_args: AsyncEngineArgs) -> "AsyncEngine":
        """Create an engine instance from `AsyncEngineArgs`.

        Args:
            engine_args (AsyncEngineArgs): Arguments required to initialize the engine.

        Returns:
            AsyncEngine: An instance of the `AsyncEngine` class.
        """
        return cls(engine_args)

    async def start(self):
        """Start the engine.

        This method sets the running flag to True, indicating that the engine
        is active and ready to process requests.
        """
        if self.running:
            logger.warning("The engine is already running.")

        self.model = SentenceTransformerEmbedder(engine_args=self.engine_args)
        self.running = True
        logger.info("Engine started.")

    async def stop(self):
        """Stop the engine.

        This method sets the running flag to False, indicating that the engine
        is no longer active and will not process requests.

        Raises:
            ValueError: If the engine is not running when this method is called.
        """
        self._check_running()
        self.running = False
        logger.info("Engine stopped.")

    def _check_running(self):
        """Check if the engine is running.

        This method verifies the running status of the engine and raises an
        error if the engine is not running.

        Raises:
            ValueError: If the engine is not running.
        """
        if not self.running:
            raise ValueError(
                "The engine is not running. "
                "You must start the engine before using it."
            )

    @property
    def engine_args(self) -> AsyncEngineArgs:
        """Get the engine arguments.

        Returns:
            AsyncEngineArgs: The arguments required to initialize the engine.
        """
        return self._engine_args

    async def aembed(self, sentences: List[str]) -> List[np.ndarray]:
        """Asynchronously embed a list of sentences.

        This method processes the input sentences using the underlying engine.
        It should only be called when the engine is running.

        Args:
            sentences (List[str]): List of sentences to be embedded.

        Raises:
            ValueError: If the engine is not running when this method is called.
        """
        self._check_running()
        embeddings = await self.model.generate_embeddings(sentences=sentences)
        return embeddings
