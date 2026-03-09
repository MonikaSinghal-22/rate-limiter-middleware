import time


class FixedWindowCounter:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size  # in seconds
        self.max_requests = max_requests
        self.counts = {}
        self.current_window_start = None

    def _get_window_start(self, timestamp: float) -> float:
        return timestamp - (timestamp % self.window_size)

    def is_allowed(self, timestamp: float = None) -> bool:
        if timestamp is None:
            timestamp = time.time()

        window_start = self._get_window_start(timestamp)

        # Reset count for new window
        if self.current_window_start != window_start:
            self.current_window_start = window_start
            self.counts = {window_start: 0}

        # Check if request is allowed
        current_count = self.counts.get(window_start, 0)
        if current_count < self.max_requests:
            self.counts[window_start] = current_count + 1
            return True
        return False
