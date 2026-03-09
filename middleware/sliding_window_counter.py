import time


class SlidingWindowCounter:
    """
    Sliding Window Counter Rate Limiter.

    Hybrid approach combining fixed window efficiency with sliding window accuracy.
    Uses weighted counts from current and previous windows.
    """

    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size  # in seconds
        self.max_requests = max_requests
        self.current_window_start = 0
        self.current_window_count = 0
        self.previous_window_count = 0

    def _get_window_start(self, timestamp: float) -> float:
        return timestamp - (timestamp % self.window_size)

    def is_allowed(self, timestamp: float = None) -> bool:
        if timestamp is None:
            timestamp = time.time()

        window_start = self._get_window_start(timestamp)

        # Handle window transition
        if window_start != self.current_window_start:
            if window_start - self.current_window_start >= self.window_size * 2:
                # More than 2 windows have passed, reset everything
                self.previous_window_count = 0
            else:
                # Move current to previous
                self.previous_window_count = self.current_window_count
            self.current_window_count = 0
            self.current_window_start = window_start

        # Calculate position in current window (0 to 1)
        position_in_window = (timestamp - window_start) / self.window_size

        # Weighted count: previous window's contribution decreases as we move through current window
        weighted_count = (
            self.previous_window_count * (1 - position_in_window)
            + self.current_window_count
        )

        if weighted_count < self.max_requests:
            self.current_window_count += 1
            return True
        return False
