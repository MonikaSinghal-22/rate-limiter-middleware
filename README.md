# Rate Limiter

A FastAPI middleware implementation featuring 5 different rate limiting algorithms. Each algorithm offers different trade-offs between accuracy, memory usage, and burst handling.

## Features

- **5 Rate Limiting Algorithms** - Choose the best fit for your use case
- **FastAPI Middleware** - Easy integration with any FastAPI application
- **Per-Client Limiting** - Rate limits applied per IP address
- **Configurable Parameters** - Customize window size, request limits, and more

## Algorithms

| Algorithm | Description | Best For |
|-----------|-------------|----------|
| **Fixed Window Counter** | Counts requests in fixed time windows | Simple use cases, low memory |
| **Sliding Window Log** | Tracks all request timestamps | Maximum accuracy |
| **Sliding Window Counter** | Weighted average of current/previous windows | Balance of accuracy & efficiency |
| **Token Bucket** | Tokens refill at a constant rate | Allowing controlled bursts |
| **Leaky Bucket** | Requests processed at constant rate | Smooth, consistent output |

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd rate-limiter

# Install dependencies
pip install -e .
# or with uv
uv sync
```

## Configuration Options

### Window-based Algorithms
(Fixed Window, Sliding Window Log, Sliding Window Counter)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `algorithm` | `RateLimiterAlgorithm` | `FIXED_WINDOW` | Algorithm to use |
| `max_requests` | `int` | `10` | Maximum requests per window |
| `window_size` | `int` | `60` | Window duration in seconds |

### Token Bucket

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `capacity` | `int` | `10` | Maximum tokens (burst size) |
| `refill_rate` | `float` | `1.0` | Tokens added per second |

### Leaky Bucket

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `capacity` | `int` | `10` | Maximum queue size |
| `leak_rate` | `float` | `1.0` | Requests processed per second |

## Usage Examples

### Fixed Window Counter
```python
app.add_middleware(
    RateLimiterMiddleware,
    algorithm=RateLimiterAlgorithm.FIXED_WINDOW,
    max_requests=100,
    window_size=60,  # 100 requests per minute
)
```

### Token Bucket (Allow Bursts)
```python
app.add_middleware(
    RateLimiterMiddleware,
    algorithm=RateLimiterAlgorithm.TOKEN_BUCKET,
    capacity=20,       # Allow burst of 20 requests
    refill_rate=2.0,   # Refill 2 tokens per second
)
```

### Leaky Bucket (Smooth Traffic)
```python
app.add_middleware(
    RateLimiterMiddleware,
    algorithm=RateLimiterAlgorithm.LEAKY_BUCKET,
    capacity=10,      # Queue up to 10 requests
    leak_rate=1.0,    # Process 1 request per second
)
```

## Running the Server

```bash
uvicorn main:app --reload
```

## Response Headers

The middleware adds these headers to responses:

| Header | Description |
|--------|-------------|
| `X-Process-Time` | Request processing time in seconds |
| `X-RateLimit-Algorithm` | Active rate limiting algorithm |
| `Retry-After` | Seconds to wait (on 429 responses) |


## License

MIT