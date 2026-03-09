import time
from enum import Enum

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from middleware.fixed_window_counter import FixedWindowCounter
from middleware.leaky_bucket import LeakyBucket
from middleware.sliding_window_counter import SlidingWindowCounter
from middleware.sliding_window_log import SlidingWindowLog
from middleware.token_bucket import TokenBucket

RateLimiter = (
    FixedWindowCounter
    | SlidingWindowLog
    | SlidingWindowCounter
    | TokenBucket
    | LeakyBucket
)


class RateLimiterAlgorithm(Enum):
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW_LOG = "sliding_window_log"
    SLIDING_WINDOW_COUNTER = "sliding_window_counter"
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        algorithm: RateLimiterAlgorithm = RateLimiterAlgorithm.FIXED_WINDOW,
        max_requests: int = 10,
        window_size: int = 60,
        # Token bucket specific
        capacity: int = 10,
        refill_rate: float = 1.0,
        # Leaky bucket specific
        leak_rate: float = 1.0,
    ):
        super().__init__(app)
        self.algorithm = algorithm
        self.max_requests = max_requests
        self.window_size = window_size
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.leak_rate = leak_rate
        self.limiters: dict[str, RateLimiter] = {}

    def _get_limiter(self, client_ip: str) -> RateLimiter:
        """Get or create a rate limiter for the client."""
        if client_ip not in self.limiters:
            if self.algorithm == RateLimiterAlgorithm.FIXED_WINDOW:
                self.limiters[client_ip] = FixedWindowCounter(
                    window_size=self.window_size, max_requests=self.max_requests
                )
            elif self.algorithm == RateLimiterAlgorithm.SLIDING_WINDOW_LOG:
                self.limiters[client_ip] = SlidingWindowLog(
                    window_size=self.window_size, max_requests=self.max_requests
                )
            elif self.algorithm == RateLimiterAlgorithm.SLIDING_WINDOW_COUNTER:
                self.limiters[client_ip] = SlidingWindowCounter(
                    window_size=self.window_size, max_requests=self.max_requests
                )
            elif self.algorithm == RateLimiterAlgorithm.TOKEN_BUCKET:
                self.limiters[client_ip] = TokenBucket(
                    capacity=self.capacity, refill_rate=self.refill_rate
                )
            elif self.algorithm == RateLimiterAlgorithm.LEAKY_BUCKET:
                self.limiters[client_ip] = LeakyBucket(
                    capacity=self.capacity, leak_rate=self.leak_rate
                )
        return self.limiters[client_ip]

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        limiter = self._get_limiter(client_ip)

        if not limiter.is_allowed():
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"Retry-After": str(self.window_size)},
            )

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-RateLimit-Algorithm"] = self.algorithm.value

        return response
