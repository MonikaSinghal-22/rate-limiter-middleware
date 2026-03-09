import time
from collections import deque


class LeakyBucket:
    """
    Leaky Bucket Rate Limiter.

    Requests are queued and processed at a fixed rate.
    Smooths out bursts by enforcing constant output rate.
    """

    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity  # max requests in queue
        self.leak_rate = leak_rate  # requests processed per second
        self.queue = deque()
        self.last_leak_time = None

    def _leak(self, timestamp: float) -> None:
        """Remove processed requests from the queue."""
        if self.last_leak_time is None:
            self.last_leak_time = timestamp
            return

        elapsed = timestamp - self.last_leak_time
        requests_to_leak = int(elapsed * self.leak_rate)

        for _ in range(min(requests_to_leak, len(self.queue))):
            self.queue.popleft()

        if requests_to_leak > 0:
            self.last_leak_time = timestamp

    def is_allowed(self, timestamp: float = None) -> bool:
        if timestamp is None:
            timestamp = time.time()

        self._leak(timestamp)

        if len(self.queue) < self.capacity:
            self.queue.append(timestamp)
            return True
        return False
