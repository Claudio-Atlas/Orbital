"""
Rate Limiting
=============
Redis-backed rate limiting to prevent abuse.

Uses sliding window algorithm:
- Each user has a counter per endpoint
- Counter expires after window passes
- Blocks requests when limit exceeded

Usage:
    @app.get("/endpoint")
    @rate_limit(requests=10, window=60)  # 10 requests per 60 seconds
    async def endpoint(user = Depends(get_current_user)):
        ...
"""

import os
import time
import functools
from typing import Optional, Callable
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

# Redis client (lazy initialization)
_redis_client = None


def get_redis():
    """Get or create Redis client."""
    global _redis_client
    
    if _redis_client is None:
        import redis
        redis_url = os.getenv("REDIS_URL")
        
        if redis_url:
            _redis_client = redis.from_url(redis_url, decode_responses=True)
        else:
            # Local development fallback - in-memory rate limiting
            _redis_client = InMemoryRateLimiter()
    
    return _redis_client


class InMemoryRateLimiter:
    """
    Fallback for local development when Redis isn't available.
    NOT for production - doesn't persist across restarts.
    """
    
    def __init__(self):
        self._counts: dict = {}
        self._expiries: dict = {}
    
    def incr(self, key: str) -> int:
        now = time.time()
        
        # Check if expired
        if key in self._expiries and self._expiries[key] < now:
            del self._counts[key]
            del self._expiries[key]
        
        # Increment
        self._counts[key] = self._counts.get(key, 0) + 1
        return self._counts[key]
    
    def expire(self, key: str, seconds: int):
        self._expiries[key] = time.time() + seconds
    
    def ttl(self, key: str) -> int:
        if key not in self._expiries:
            return -1
        remaining = int(self._expiries[key] - time.time())
        return max(0, remaining)
    
    def get(self, key: str) -> Optional[str]:
        now = time.time()
        if key in self._expiries and self._expiries[key] < now:
            return None
        return str(self._counts.get(key, 0))


class RateLimitExceeded(HTTPException):
    """Custom exception for rate limiting."""
    
    def __init__(self, retry_after: int):
        super().__init__(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many requests. Please slow down.",
                "retry_after": retry_after
            },
            headers={"Retry-After": str(retry_after)}
        )


def rate_limit(
    requests: int = 10,
    window: int = 60,
    key_func: Optional[Callable] = None
):
    """
    Rate limiting decorator for FastAPI endpoints.
    
    Args:
        requests: Maximum requests allowed in window
        window: Time window in seconds
        key_func: Optional function to extract rate limit key from request
                  Default: uses user ID from auth
    
    Example:
        @app.post("/solve")
        @rate_limit(requests=5, window=60)  # 5 per minute
        async def solve(...):
            ...
    """
    
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user from kwargs (set by Depends(get_current_user))
            user = kwargs.get("user")
            
            if user is None:
                # No user = no rate limiting (endpoint should require auth anyway)
                return await func(*args, **kwargs)
            
            # Build rate limit key
            user_id = user.get("sub", user.get("id", "anonymous"))
            endpoint = func.__name__
            key = f"rate_limit:{user_id}:{endpoint}"
            
            # Check rate limit
            redis = get_redis()
            
            try:
                # Increment counter
                current = redis.incr(key)
                
                # Set expiry on first request
                if current == 1:
                    redis.expire(key, window)
                
                # Check if exceeded
                if current > requests:
                    retry_after = redis.ttl(key)
                    if retry_after < 0:
                        retry_after = window
                    raise RateLimitExceeded(retry_after=retry_after)
                
                # Add rate limit headers to response
                response = await func(*args, **kwargs)
                
                # If response is a dict/model, we can't add headers easily
                # Headers are added for 429 responses via RateLimitExceeded
                return response
                
            except RateLimitExceeded:
                raise
            except Exception as e:
                # Redis error - fail open (allow request but log warning)
                from utils.logging import logger, log_security_event
                from utils.alerts import alert_error
                
                log_security_event(
                    "rate_limit_redis_error",
                    f"Redis error, failing open: {e}",
                    user_id=user_id
                )
                alert_error("Rate limit Redis error - failing open", error=str(e)[:200])
                
                # In production, you might want to fail closed instead:
                # raise HTTPException(503, "Service temporarily unavailable")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def check_rate_limit(user_id: str, endpoint: str, requests: int = 10, window: int = 60) -> bool:
    """
    Check rate limit without incrementing (for pre-flight checks).
    
    Returns:
        True if request would be allowed, False if would be blocked
    """
    redis = get_redis()
    key = f"rate_limit:{user_id}:{endpoint}"
    
    try:
        current = redis.get(key)
        if current is None:
            return True
        return int(current) < requests
    except Exception:
        return True  # Fail open


def get_rate_limit_status(user_id: str, endpoint: str, requests: int = 10, window: int = 60) -> dict:
    """
    Get current rate limit status for debugging/headers.
    
    Returns:
        {
            "limit": 10,
            "remaining": 7,
            "reset": 45  # seconds until reset
        }
    """
    redis = get_redis()
    key = f"rate_limit:{user_id}:{endpoint}"
    
    try:
        current = redis.get(key)
        ttl = redis.ttl(key)
        
        if current is None:
            return {"limit": requests, "remaining": requests, "reset": 0}
        
        current = int(current)
        remaining = max(0, requests - current)
        reset = max(0, ttl) if ttl > 0 else window
        
        return {"limit": requests, "remaining": remaining, "reset": reset}
    except Exception:
        return {"limit": requests, "remaining": requests, "reset": 0}
