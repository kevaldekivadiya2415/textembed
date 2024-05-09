import asyncio
import time
import ray
from functools import partial
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)
from sentence_transformers import SentenceTransformer

# Initialize Ray
ray.init()


# Define a remote function to load the Sentence Transformer model
@ray.remote(num_cpus=1)
def load_sentence_transformer_model():
    # Load the Sentence Transformer model
    model = SentenceTransformer("bert-base-nli-mean-tokens")
    return model


# Define a function to raise an exception on task finish
def raise_exception_on_finish(
    task: asyncio.Task, error_callback: Callable[[Exception], None]
) -> None:
    msg = "Task finished unexpectedly. This should never happen! Please open an issue on Github."

    exception = None
    try:
        task.result()
        # This will be thrown if task exits normally (which it should not)
        raise RuntimeError(msg)
    except Exception as e:
        exception = e
        error_callback(exception)
        raise RuntimeError(msg + " See stack trace above for the actual cause.") from e


# Define a class to handle asynchronous loading and processing
class AsyncSentenceTransformerEngine:
    def __init__(self):
        self.model_ref = None
        self.background_loop = None

    async def load_model(self):
        # Load the Sentence Transformer model asynchronously
        self.model_ref = await load_sentence_transformer_model.remote()

    async def start_background_loop(self):
        # Load the Sentence Transformer model
        await self.load_model()
        self.model = ray.get(self.model_ref)

        # Use the model to process requests or perform other tasks
        while True:
            # Implement your processing logic here
            await asyncio.sleep(1)  # Placeholder for actual processing logic

    def start(self):
        # Start the background loop
        if self.background_loop is None:
            self.background_loop = asyncio.get_event_loop().create_task(
                self.start_background_loop()
            )
            self.background_loop.add_done_callback(
                partial(raise_exception_on_finish, error_callback=self.error_callback)
            )

    def error_callback(self, exc: Exception) -> None:
        print(f"Error occurred in background loop: {exc}")


# Usage
if __name__ == "__main__":
    engine = AsyncSentenceTransformerEngine()
    engine.start()
    asyncio.run(engine.start_background_loop())
