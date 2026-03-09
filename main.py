from fastapi import FastAPI

from middleware.ratelimiter import RateLimiterAlgorithm, RateLimiterMiddleware

app = FastAPI()

# Choose your rate limiting algorithm:

# Option 1: Fixed Window Counter (default)
app.add_middleware(
    RateLimiterMiddleware,
    algorithm=RateLimiterAlgorithm.FIXED_WINDOW,
    max_requests=10,
    window_size=60,
)

# Option 2: Sliding Window Log (most accurate)
# app.add_middleware(
#     RateLimiterMiddleware,
#     algorithm=RateLimiterAlgorithm.SLIDING_WINDOW_LOG,
#     max_requests=10,
#     window_size=60,
# )

# Option 3: Sliding Window Counter (balanced)
# app.add_middleware(
#     RateLimiterMiddleware,
#     algorithm=RateLimiterAlgorithm.SLIDING_WINDOW_COUNTER,
#     max_requests=10,
#     window_size=60,
# )

# Option 4: Token Bucket (allows bursts)
# app.add_middleware(
#     RateLimiterMiddleware,
#     algorithm=RateLimiterAlgorithm.TOKEN_BUCKET,
#     capacity=10,
#     refill_rate=1.0,  # 1 token per second
# )

# Option 5: Leaky Bucket (smooth output)
# app.add_middleware(
#     RateLimiterMiddleware,
#     algorithm=RateLimiterAlgorithm.LEAKY_BUCKET,
#     capacity=10,
#     leak_rate=1.0,  # process 1 request per second
# )


@app.get("/")
async def main():
    return {"message": "Hello, World!"}
