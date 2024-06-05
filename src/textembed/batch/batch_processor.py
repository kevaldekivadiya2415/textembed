"""Batch Processor"""

import asyncio
import time
from asyncio import Queue
from typing import List

from textembed.executor.embedder.sentence_transformer import SentenceTransformerEmbedder
from textembed.log import logger


class BatchProcessor:
    """Batch Processor for handling asynchronous text embedding requests.

    This class manages a queue of embedding requests and processes them in batches
    using multiple worker tasks.

    Attributes:
        model (SentenceTransformerEmbedder): The model used for generating embeddings.
        workers (int): The number of worker tasks to process requests.
        batch_size (int): The maximum number of requests to process in a single batch.
        request_queue (Queue): The queue holding incoming embedding requests.
        loop (asyncio.AbstractEventLoop): The event loop used to create worker tasks.
        worker_tasks (List[asyncio.Task]): The list of worker tasks.
    """

    def __init__(
        self,
        model: SentenceTransformerEmbedder,
        workers: int,
        batch_size: int,
    ) -> None:
        """Initialize the BatchProcessor with the given model, number of workers, and batch size.

        Args:
            model (SentenceTransformerEmbedder): The model used for generating embeddings.
            workers (int): The number of worker tasks to process requests.
            batch_size (int): The maximum number of requests to process in a single batch.
        """
        self.model = model
        self.workers = workers
        self.batch_size = batch_size
        self.request_queue: Queue = Queue()
        self.loop = asyncio.get_running_loop()
        self.worker_tasks = [
            self.loop.create_task(self.batch_processor(i)) for i in range(workers)
        ]
        # Wait until all worker tasks are started
        self.loop.create_task(self._log_workers_started())

    async def _log_workers_started(self):
        await asyncio.sleep(0)  # Yield control to ensure workers have started
        logger.info(
            "All %d workers have started batch processing for the %s model.",
            self.workers,
            self.model.engine_args.model,
        )

    async def batch_processor(self, worker_id: int):
        """Worker task that processes requests from the queue in batches.

        Args:
            worker_id (int): The identifier for the worker task.
        """
        logger.debug(
            "Worker with ID %d has started batch processing for the %s model.",
            worker_id,
            self.model.engine_args.model,
        )
        while True:
            start_time = time.perf_counter()
            requests = []
            try:
                while len(requests) < self.batch_size:
                    request = await asyncio.wait_for(
                        self.request_queue.get(), timeout=0.05
                    )
                    requests.append(request)
            except asyncio.TimeoutError:
                pass

            if requests:
                all_texts = [
                    text for req in requests for text in req[0]
                ]  # Flatten list of lists
                futures = [req[1] for req in requests]

                try:
                    embeddings, usage = await self.model.process_batch(all_texts)
                    # Split embeddings back to individual futures
                    idx = 0
                    for future, req in zip(futures, requests):
                        num_texts = len(req[0])
                        future.set_result(
                            (
                                embeddings[idx : idx + num_texts],
                                usage[idx : idx + num_texts],
                            )
                        )
                        idx += num_texts
                except Exception as e:
                    for future in futures:
                        future.set_exception(e)

                logger.debug(
                    "Worker %d processed batch in %.4f ms",
                    worker_id,
                    (time.perf_counter() - start_time) * 1000,
                )

    async def add_request(self, texts: List[str], future: asyncio.Future):
        """Add a new embedding request to the queue.

        Args:
            texts (List[str]): List of sentences to be embedded.
            future (asyncio.Future): Future object to set the result of embeddings.
        """
        await self.request_queue.put((texts, future))

    async def shutdown(self):
        """Shutdown the batch processor by cancelling all worker tasks."""
        for task in self.worker_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logger.info("Worker task cancelled.")
