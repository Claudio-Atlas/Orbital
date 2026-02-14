"""
Structured Logging
==================
JSON-formatted logging for Railway and local development.

Security:
- NEVER log tokens, API keys, emails, or problem content
- User IDs are partially masked (first 8 chars only)
- Request bodies are NOT logged

Usage:
    from utils.logging import logger, log_request, log_error

    logger.info("Job started", extra={"job_id": job_id})
    logger.error("Job failed", extra={"job_id": job_id, "error": str(e)})
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime, timezone
from typing import Any, Optional
from contextvars import ContextVar

# Context variable for request-scoped data
request_context: ContextVar[dict] = ContextVar("request_context", default={})


class JSONFormatter(logging.Formatter):
    """
    Formats log records as JSON for structured logging.
    Railway and most log aggregators parse JSON automatically.
    """
    
    # Fields that should never appear in logs (security)
    REDACTED_FIELDS = {
        "token", "jwt", "bearer", "authorization", "auth",
        "api_key", "apikey", "secret", "password", "credential",
        "email", "phone", "problem", "image", "content", "body"
    }
    
    def format(self, record: logging.LogRecord) -> str:
        # Base log structure
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add request context if available
        ctx = request_context.get()
        if ctx:
            log_entry["request_id"] = ctx.get("request_id")
            if ctx.get("user_id"):
                # Mask user ID - only first 8 chars
                log_entry["user_id"] = ctx["user_id"][:8] + "..." if len(ctx["user_id"]) > 8 else ctx["user_id"]
            if ctx.get("path"):
                log_entry["path"] = ctx["path"]
            if ctx.get("method"):
                log_entry["method"] = ctx["method"]
        
        # Add extra fields (from logger.info(..., extra={...}))
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in {
                    "name", "msg", "args", "created", "filename", "funcName",
                    "levelname", "levelno", "lineno", "module", "msecs",
                    "pathname", "process", "processName", "relativeCreated",
                    "stack_info", "exc_info", "exc_text", "thread", "threadName",
                    "message", "taskName"
                }:
                    # Security: redact sensitive fields
                    if any(sensitive in key.lower() for sensitive in self.REDACTED_FIELDS):
                        log_entry[key] = "[REDACTED]"
                    else:
                        log_entry[key] = self._safe_serialize(value)
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self._format_traceback(record.exc_info)
            }
        
        return json.dumps(log_entry, default=str)
    
    def _safe_serialize(self, value: Any) -> Any:
        """Safely serialize values, handling non-JSON-serializable types."""
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        if isinstance(value, (list, tuple)):
            return [self._safe_serialize(v) for v in value[:10]]  # Limit array size
        if isinstance(value, dict):
            return {k: self._safe_serialize(v) for k, v in list(value.items())[:20]}  # Limit dict size
        return str(value)
    
    def _format_traceback(self, exc_info) -> Optional[str]:
        """Format traceback, limiting length."""
        if not exc_info or not exc_info[2]:
            return None
        tb_lines = traceback.format_exception(*exc_info)
        tb_str = "".join(tb_lines)
        # Limit traceback length
        if len(tb_str) > 2000:
            tb_str = tb_str[:2000] + "\n... [truncated]"
        return tb_str


class ConsoleFormatter(logging.Formatter):
    """
    Human-readable formatter for local development.
    Uses colors when running in a terminal.
    """
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        # Check if we should use colors
        use_colors = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
        
        level = record.levelname
        if use_colors:
            level = f"{self.COLORS.get(level, '')}{level}{self.RESET}"
        
        # Get request context
        ctx = request_context.get()
        request_id = ctx.get("request_id", "-")[:8] if ctx.get("request_id") else "-"
        
        # Format: [TIME] LEVEL [REQ_ID] message
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] {level:8} [{request_id}] {record.getMessage()}"


def setup_logger(name: str = "orbital") -> logging.Logger:
    """
    Create and configure the application logger.
    
    Uses JSON format in production (Railway), console format in development.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Determine environment
    is_production = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PRODUCTION")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    
    if is_production:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(ConsoleFormatter())
    
    logger.addHandler(handler)
    
    # Don't propagate to root logger
    logger.propagate = False
    
    return logger


# Create the default logger
logger = setup_logger()


# ============================================
# Convenience Functions
# ============================================

def set_request_context(
    request_id: str,
    user_id: Optional[str] = None,
    path: Optional[str] = None,
    method: Optional[str] = None
):
    """Set context for the current request (used by middleware)."""
    request_context.set({
        "request_id": request_id,
        "user_id": user_id,
        "path": path,
        "method": method
    })


def clear_request_context():
    """Clear request context (used by middleware after response)."""
    request_context.set({})


def log_request_start(method: str, path: str, user_id: Optional[str] = None):
    """Log the start of a request."""
    logger.info(
        f"{method} {path}",
        extra={
            "event": "request_start",
            "user_id_partial": user_id[:8] + "..." if user_id and len(user_id) > 8 else user_id
        }
    )


def log_request_end(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: Optional[str] = None
):
    """Log the end of a request with timing."""
    level = logging.INFO if status_code < 400 else logging.WARNING if status_code < 500 else logging.ERROR
    
    logger.log(
        level,
        f"{method} {path} → {status_code} ({duration_ms:.0f}ms)",
        extra={
            "event": "request_end",
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
            "user_id_partial": user_id[:8] + "..." if user_id and len(user_id) > 8 else user_id
        }
    )


def log_job_event(
    job_id: str,
    event: str,
    user_id: Optional[str] = None,
    **extra
):
    """Log a job lifecycle event."""
    logger.info(
        f"Job {event}: {job_id[:8]}...",
        extra={
            "event": f"job_{event}",
            "job_id": job_id,
            "user_id_partial": user_id[:8] + "..." if user_id and len(user_id) > 8 else user_id,
            **extra
        }
    )


def log_error(
    message: str,
    error: Optional[Exception] = None,
    **extra
):
    """Log an error with optional exception."""
    logger.error(
        message,
        exc_info=error is not None,
        extra={
            "event": "error",
            "error_type": type(error).__name__ if error else None,
            "error_message": str(error) if error else None,
            **extra
        }
    )


def log_security_event(
    event_type: str,
    message: str,
    user_id: Optional[str] = None,
    **extra
):
    """Log a security-relevant event (rate limit, auth failure, etc.)."""
    logger.warning(
        f"[SECURITY] {event_type}: {message}",
        extra={
            "event": f"security_{event_type}",
            "user_id_partial": user_id[:8] + "..." if user_id and len(user_id) > 8 else user_id,
            **extra
        }
    )
