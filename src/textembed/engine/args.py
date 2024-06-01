"""Engine arguments"""

import multiprocessing
from dataclasses import dataclass
from typing import Optional


@dataclass
class AsyncEngineArgs:
    """A dataclass representing the arguments required to initialize an asynchronous engine.

    Attributes:
        model (str): The path or identifier of the model to be used by the engine.
        served_model_name (Optional[str]): An optional name to be used for serving the model.
                                            Default is `model` name
        trust_remote_code (bool): Whether to trust remote code.
        workers (int): The number of worker tasks to process requests. Defaults to the number of CPU cores.
        batch_size (int): The maximum number of requests to process in a single batch.
                          Must be greater than or equal to 1.
        embedding_dtype(str): Embedding data type for final generate embedding.
    """

    model: str
    served_model_name: Optional[str] = None
    trust_remote_code: bool = True
    workers: int = multiprocessing.cpu_count()
    batch_size: int = 32
    embedding_dtype: str = "float32"

    def __post_init__(self):
        # If served_model_name is not provided, derive it from the model path
        if self.served_model_name is None:
            self.served_model_name = self.model

        # Ensure the batch size is valid
        if self.batch_size < 1:
            raise ValueError("Batch size must be greater than or equal to 1.")

        # Ensure the number of workers is valid
        if self.workers < 1:
            raise ValueError("Number of workers must be greater than or equal to 1.")
