import multiprocessing
from functools import lru_cache, wraps

import ray

from textembed.engine.args import AsyncEngineArgs
from textembed.executor.ray_cpu import ModelActor
from textembed.executor.ray_utils import initialize_ray_cluster
from textembed.log import logger


class AsyncEngine:
    def __init__(self, engine_args: AsyncEngineArgs) -> None:
        self._engine_args = engine_args
        self.running = False

    @classmethod
    def from_args(cls, engine_args: AsyncEngineArgs) -> "AsyncEngine":
        """Create an engine from AsyncEngineArgs."""
        return cls(engine_args)

    async def start(self):
        """Start the engine."""

        if self.running:
            logger.warning("The engine is already running.")
            return

        # Initialize Ray cluster
        initialize_ray_cluster(world_size=multiprocessing.cpu_count())
        self.model_actors = [ModelActor.remote() for _ in range(2)]
        logger.info("Model loaded.")

        self.running = True
        logger.info("Engine started.")

    async def stop(self):
        """Stop the engine."""
        self._check_running()
        self.running = False
        logger.info("Engine stopped.")

    def _check_running(self):
        if not self.running:
            raise ValueError(
                "The engine is not running. "
                "You should start the engine before using it."
            )

    @property
    def engine_args(self) -> AsyncEngineArgs:
        """Get the engine arguments."""
        return self._engine_args

    def list_to_tuple(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            # Call the function and await the result
            result = await function(*args, **kwargs)
            # Convert list elements to tuples
            if isinstance(result, list):
                result = [tuple(x) if isinstance(x, list) else x for x in result]
            elif isinstance(result, tuple):
                result = tuple(
                    x if not isinstance(x, list) else tuple(x) for x in result
                )
            return result

        return wrapper

    @list_to_tuple
    @lru_cache(maxsize=128, typed=False)
    async def aembed(self, sentences: list[str]):
        self._check_running()
        embeddings = ray.get(
            [actor.encode_sentences.remote(sentences) for actor in self.model_actors]
        )
        return embeddings[0]
