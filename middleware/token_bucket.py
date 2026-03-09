import time


class TokenBucket:
    """
    Token Bucket Rate Limiter.

    Tokens are added at a fixed rate up to a maximum capacity.
    Each request consumes one token. Allows bursts up to bucket capacity.
    """

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity  # max tokens in bucket
        self.refill_rate = refill_rate  # tokens added per second
        self.tokens = capacity
        self.last_refill_time = None

    def _refill(self, timestamp: float) -> None:
        """Add tokens based on elapsed time."""
        if self.last_refill_time is None:
            self.last_refill_time = timestamp
            return

        elapsed = timestamp - self.last_refill_time
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = timestamp

    def is_allowed(self, timestamp: float = None, tokens_requested: int = 1) -> bool:
        if timestamp is None:
            timestamp = time.time()

        self._refill(timestamp)

        if self.tokens >= tokens_requested:
            self.tokens -= tokens_requested
            return True
        return False
