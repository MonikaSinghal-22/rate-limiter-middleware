import time
from collections import deque


class SlidingWindowLog:
    """
    Sliding Window Log Rate Limiter.

    Tracks timestamps of all requests within the window.
    More accurate than fixed window but uses more memory.
    """

    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size  # in seconds
        self.max_requests = max_requests
        self.request_log = deque()

    def _cleanup_old_requests(self, timestamp: float) -> None:
        """Remove requests outside the current window."""
        window_start = timestamp - self.window_size
        while self.request_log and self.request_log[0] <= window_start:
            self.request_log.popleft()

    def is_allowed(self, timestamp: float = None) -> bool:
        if timestamp is None:
            timestamp = time.time()

        self._cleanup_old_requests(timestamp)

        if len(self.request_log) < self.max_requests:
            self.request_log.append(timestamp)
            return True
        return False
