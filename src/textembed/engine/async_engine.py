"""Asynchronous engine creation."""

from typing import List

from textembed.batch import BatchProcessor
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
        batch_processor (BatchProcessor): Processor for handling batch requests.
        model (SentenceTransformerEmbedder): Model for generating embeddings.
    """

    def __init__(self, engine_args: AsyncEngineArgs) -> None:
        """
        Initialize the asynchronous engine.

        Args:
            engine_args (AsyncEngineArgs): Arguments required to initialize the engine.
        """
        self._engine_args = engine_args
        self.running = False
        self.batch_processor = None
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

        This method initializes the model and batch processor, and sets the
        running flag to True, indicating that the engine is active and ready
        to process requests.
        """
        if self.running:
            logger.warning("The engine is already running.")
            return

        self.model = SentenceTransformerEmbedder(engine_args=self._engine_args)
        self.batch_processor = BatchProcessor(
            model=self.model,
            workers=self._engine_args.workers,
            batch_size=self._engine_args.batch_size,
        )
        self.running = True
        logger.info("Engine started for the %s model.", self._engine_args.model)

        # Warm-up the model
        await self.model.warm_up()

    async def stop(self):
        """Stop the engine.

        This method sets the running flag to False, indicating that the engine
        is no longer active and will not process requests.

        Raises:
            ValueError: If the engine is not running when this method is called.
        """
        self._check_running()
        self.running = False
        if self.batch_processor is not None:
            await self.batch_processor.shutdown()
        logger.info("Engine stopped for the %s model.", self._engine_args.model)

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

    async def aembed(self, sentences: List[str], future):
        """Asynchronously embed a list of sentences.

        This method processes the input sentences using the underlying engine.
        It should only be called when the engine is running.

        Args:
            sentences (List[str]): List of sentences to be embedded.
            future (asyncio.Future): A future object to set the result of embeddings.

        Raises:
            ValueError: If the engine is not running when this method is called.
        """
        self._check_running()
        if self.batch_processor is None:
            raise ValueError("Batch processor is not initialized.")
        await self.batch_processor.add_request(sentences, future)
