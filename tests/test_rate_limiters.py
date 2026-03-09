"""Tests for rate limiter algorithms."""

from middleware.fixed_window_counter import FixedWindowCounter
from middleware.leaky_bucket import LeakyBucket
from middleware.sliding_window_counter import SlidingWindowCounter
from middleware.sliding_window_log import SlidingWindowLog
from middleware.token_bucket import TokenBucket


class TestFixedWindowCounter:
    def test_allows_requests_under_limit(self):
        limiter = FixedWindowCounter(window_size=60, max_requests=5)
        base_time = 1000.0

        for i in range(5):
            assert limiter.is_allowed(base_time + i) is True

    def test_blocks_requests_over_limit(self):
        limiter = FixedWindowCounter(window_size=60, max_requests=5)
        base_time = 1000.0

        for i in range(5):
            limiter.is_allowed(base_time + i)

        assert limiter.is_allowed(base_time + 5) is False

    def test_resets_on_new_window(self):
        limiter = FixedWindowCounter(window_size=60, max_requests=5)

        for i in range(5):
            limiter.is_allowed(1000.0 + i)

        # New window
        assert limiter.is_allowed(1060.0) is True


class TestSlidingWindowLog:
    def test_allows_requests_under_limit(self):
        limiter = SlidingWindowLog(window_size=60, max_requests=5)
        base_time = 1000.0

        for i in range(5):
            assert limiter.is_allowed(base_time + i) is True

    def test_blocks_requests_over_limit(self):
        limiter = SlidingWindowLog(window_size=60, max_requests=5)
        base_time = 1000.0

        for i in range(5):
            limiter.is_allowed(base_time + i)

        assert limiter.is_allowed(base_time + 5) is False

    def test_allows_after_window_passes(self):
        limiter = SlidingWindowLog(window_size=60, max_requests=5)

        for i in range(5):
            limiter.is_allowed(1000.0 + i)

        # After window passes
        assert limiter.is_allowed(1061.0) is True


class TestSlidingWindowCounter:
    def test_allows_requests_under_limit(self):
        limiter = SlidingWindowCounter(window_size=60, max_requests=5)
        base_time = 1000.0

        for i in range(5):
            assert limiter.is_allowed(base_time + i) is True

    def test_blocks_requests_over_limit(self):
        limiter = SlidingWindowCounter(window_size=60, max_requests=5)
        base_time = 1000.0

        for i in range(5):
            limiter.is_allowed(base_time + i)

        assert limiter.is_allowed(base_time + 5) is False


class TestTokenBucket:
    def test_allows_burst_up_to_capacity(self):
        limiter = TokenBucket(capacity=5, refill_rate=1.0)
        base_time = 1000.0

        for _ in range(5):
            assert limiter.is_allowed(base_time) is True

    def test_blocks_after_capacity_exhausted(self):
        limiter = TokenBucket(capacity=5, refill_rate=1.0)
        base_time = 1000.0

        for _ in range(5):
            limiter.is_allowed(base_time)

        assert limiter.is_allowed(base_time) is False

    def test_refills_over_time(self):
        limiter = TokenBucket(capacity=5, refill_rate=1.0)

        for _ in range(5):
            limiter.is_allowed(1000.0)

        # After 2 seconds, should have 2 tokens
        assert limiter.is_allowed(1002.0) is True
        assert limiter.is_allowed(1002.0) is True
        assert limiter.is_allowed(1002.0) is False


class TestLeakyBucket:
    def test_allows_requests_under_capacity(self):
        limiter = LeakyBucket(capacity=5, leak_rate=1.0)
        base_time = 1000.0

        for i in range(5):
            assert limiter.is_allowed(base_time + i) is True

    def test_blocks_when_queue_full(self):
        limiter = LeakyBucket(capacity=5, leak_rate=1.0)
        base_time = 1000.0

        for _ in range(5):
            limiter.is_allowed(base_time)

        assert limiter.is_allowed(base_time) is False

    def test_leaks_over_time(self):
        limiter = LeakyBucket(capacity=5, leak_rate=1.0)

        for _ in range(5):
            limiter.is_allowed(1000.0)

        # After 3 seconds, 3 requests should have leaked
        assert limiter.is_allowed(1003.0) is True
