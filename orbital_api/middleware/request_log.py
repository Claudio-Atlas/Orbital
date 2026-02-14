"""
Request Logging Middleware
==========================
Logs all incoming requests with timing, status, and context.

Security:
- Does NOT log request bodies (may contain problem text)
- Does NOT log full user IDs
- Does NOT log authorization headers
- DOES log: path, method, status, duration, partial user ID
"""

import time
import uuid
from typing import Callable, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from utils.logging import (
    logger,
    set_request_context,
    clear_request_context,
    log_request_start,
    log_request_end
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs every request with timing information.
    
    Features:
    - Assigns unique request_id to each request
    - Logs start and end of request
    - Tracks response time
    - Sets request context for other loggers to use
    """
    
    # Paths to skip logging (health checks, static files)
    SKIP_PATHS = {"/health", "/favicon.ico", "/robots.txt"}
    
    # Paths to log at DEBUG level (high frequency, low value)
    DEBUG_PATHS = {"/metrics"}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip logging for certain paths
        path = request.url.path
        if path in self.SKIP_PATHS:
            return await call_next(request)
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Extract user ID from JWT if present (safely)
        user_id = self._extract_user_id(request)
        
        # Set request context for other loggers
        set_request_context(
            request_id=request_id,
            user_id=user_id,
            path=path,
            method=request.method
        )
        
        # Add request ID to response headers
        start_time = time.perf_counter()
        
        # Log request start (skip for debug paths)
        if path not in self.DEBUG_PATHS:
            log_request_start(request.method, path, user_id)
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Log request end
            if path not in self.DEBUG_PATHS:
                log_request_end(
                    request.method,
                    path,
                    response.status_code,
                    duration_ms,
                    user_id
                )
            
            # Add headers to response
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration_ms:.0f}ms"
            
            return response
            
        except Exception as e:
            # Log error and re-raise
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"Request failed: {request.method} {path}",
                exc_info=True,
                extra={
                    "event": "request_error",
                    "duration_ms": round(duration_ms, 2),
                    "error_type": type(e).__name__
                }
            )
            raise
            
        finally:
            # Clear request context
            clear_request_context()
    
    def _extract_user_id(self, request: Request) -> Optional[str]:
        """
        Safely extract user ID from request.
        Does NOT validate JWT - just extracts sub claim for logging.
        
        Security: We only extract, never trust this for auth decisions.
        """
        auth_header = request.headers.get("authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header[7:]  # Remove "Bearer "
        
        try:
            # JWT is base64 encoded, we just need the payload
            import base64
            import json
            
            # Split token and get payload (middle part)
            parts = token.split(".")
            if len(parts) != 3:
                return None
            
            # Decode payload (add padding if needed)
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding
            
            decoded = base64.urlsafe_b64decode(payload)
            claims = json.loads(decoded)
            
            return claims.get("sub")
            
        except Exception:
            # Any error - just return None, don't log (could be attack)
            return None
