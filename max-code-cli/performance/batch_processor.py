"""
Request batching for improved throughput.
Combines multiple requests into single backend call.
"""

import asyncio
from typing import Any, Callable, List
from dataclasses import dataclass, field
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class BatchRequest:
    """Single request in a batch."""

    id: str
    data: Any
    future: asyncio.Future = field(default_factory=asyncio.Future)


class BatchProcessor:
    """
    Process requests in batches for improved throughput.

    Benefits:
    - Reduced network overhead (1 request vs N requests)
    - Better backend resource utilization
    - Lower latency for individual requests
    """

    def __init__(
        self,
        batch_size: int = 10,
        batch_timeout: float = 0.1,
        processor: Callable = None,
    ):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.processor = processor
        self.queue: List[BatchRequest] = []
        self.lock = asyncio.Lock()
        self._processing = False

    async def submit(self, request_id: str, data: Any) -> Any:
        """Submit request to batch processor."""
        request = BatchRequest(id=request_id, data=data)

        async with self.lock:
            self.queue.append(request)
            logger.debug("batch_request_added", id=request_id, queue_size=len(self.queue))

            # Start processing if not already running
            if not self._processing:
                asyncio.create_task(self._process_batch())

        # Wait for result
        return await request.future

    async def _process_batch(self):
        """Process batch of requests."""
        self._processing = True

        # Wait for batch to fill or timeout
        await asyncio.sleep(self.batch_timeout)

        async with self.lock:
            if not self.queue:
                self._processing = False
                return

            # Take batch
            batch = self.queue[: self.batch_size]
            self.queue = self.queue[self.batch_size :]

            logger.info("batch_processing", batch_size=len(batch))

        # Process batch
        try:
            results = await self.processor([r.data for r in batch])

            # Set results
            for request, result in zip(batch, results):
                request.future.set_result(result)

            logger.info("batch_processed", batch_size=len(batch))

        except Exception as e:
            logger.error("batch_processing_error", error=str(e))
            for request in batch:
                request.future.set_exception(e)

        finally:
            self._processing = False

            # Process remaining queue
            if self.queue:
                asyncio.create_task(self._process_batch())


# Usage example
"""
async def process_batch_function(items: List[Any]) -> List[Any]:
    # Process multiple items at once
    return await backend.batch_analyze(items)

batch_processor = BatchProcessor(
    batch_size=10,
    batch_timeout=0.1,
    processor=process_batch_function
)

# Submit requests
result = await batch_processor.submit("req_1", {"code": "..."})
"""
