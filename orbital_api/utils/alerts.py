"""
Alerting
========
Simple webhook-based alerting for errors and critical events.

Supports:
- Discord webhooks
- Slack webhooks
- Generic webhooks

Configuration:
- ALERT_WEBHOOK_URL: Discord or Slack webhook URL
- ALERT_LEVEL: Minimum level to alert (ERROR, CRITICAL). Default: ERROR
- ALERT_ENABLED: Set to "false" to disable. Default: true

Usage:
    from utils.alerts import alert_error, alert_critical

    alert_error("Payment webhook failed", job_id="abc123")
    alert_critical("Database connection lost")
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
from enum import Enum

import httpx

from utils.logging import logger


class AlertLevel(Enum):
    ERROR = "error"
    CRITICAL = "critical"


# Configuration
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")
ALERT_LEVEL = os.getenv("ALERT_LEVEL", "ERROR").upper()
ALERT_ENABLED = os.getenv("ALERT_ENABLED", "true").lower() != "false"
ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", "development")

# Rate limiting for alerts (don't spam)
_last_alert_time: dict[str, float] = {}
ALERT_COOLDOWN_SECONDS = 60  # Same alert type only once per minute


def _should_send_alert(alert_key: str) -> bool:
    """Check if we should send this alert (rate limiting)."""
    import time
    
    now = time.time()
    last_time = _last_alert_time.get(alert_key, 0)
    
    if now - last_time < ALERT_COOLDOWN_SECONDS:
        return False
    
    _last_alert_time[alert_key] = now
    return True


def _detect_webhook_type(url: str) -> str:
    """Detect if webhook is Discord, Slack, or generic."""
    if not url:
        return "none"
    if "discord.com/api/webhooks" in url or "discordapp.com/api/webhooks" in url:
        return "discord"
    if "hooks.slack.com" in url:
        return "slack"
    return "generic"


def _format_discord_payload(
    level: AlertLevel,
    message: str,
    details: Optional[dict] = None
) -> dict:
    """Format alert as Discord embed."""
    color = 0xFF0000 if level == AlertLevel.CRITICAL else 0xFFA500  # Red or Orange
    
    embed = {
        "title": f"🚨 {level.value.upper()}: Orbital Alert",
        "description": message,
        "color": color,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "footer": {"text": f"Environment: {ENVIRONMENT}"}
    }
    
    if details:
        embed["fields"] = [
            {"name": k, "value": str(v)[:1024], "inline": True}
            for k, v in list(details.items())[:10]  # Limit fields
        ]
    
    return {"embeds": [embed]}


def _format_slack_payload(
    level: AlertLevel,
    message: str,
    details: Optional[dict] = None
) -> dict:
    """Format alert as Slack message."""
    emoji = "🔴" if level == AlertLevel.CRITICAL else "🟠"
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{emoji} {level.value.upper()}: Orbital Alert"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": message
            }
        }
    ]
    
    if details:
        detail_text = "\n".join(f"*{k}:* {v}" for k, v in list(details.items())[:10])
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": detail_text
            }
        })
    
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"Environment: {ENVIRONMENT} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
            }
        ]
    })
    
    return {"blocks": blocks}


def _format_generic_payload(
    level: AlertLevel,
    message: str,
    details: Optional[dict] = None
) -> dict:
    """Format alert as generic JSON payload."""
    return {
        "level": level.value,
        "message": message,
        "details": details or {},
        "environment": ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "orbital-api"
    }


async def send_alert_async(
    level: AlertLevel,
    message: str,
    details: Optional[dict] = None,
    alert_key: Optional[str] = None
) -> bool:
    """
    Send an alert asynchronously.
    
    Args:
        level: ERROR or CRITICAL
        message: Human-readable message
        details: Optional dict of additional context
        alert_key: Optional key for rate limiting (defaults to message hash)
    
    Returns:
        True if sent, False if skipped or failed
    """
    # Check if alerting is enabled
    if not ALERT_ENABLED or not ALERT_WEBHOOK_URL:
        logger.debug("Alerting disabled or no webhook configured")
        return False
    
    # Check alert level threshold
    if level == AlertLevel.ERROR and ALERT_LEVEL == "CRITICAL":
        return False  # Only critical alerts enabled
    
    # Rate limiting
    key = alert_key or message[:100]
    if not _should_send_alert(key):
        logger.debug(f"Alert rate limited: {key[:50]}...")
        return False
    
    # Format payload based on webhook type
    webhook_type = _detect_webhook_type(ALERT_WEBHOOK_URL)
    
    if webhook_type == "discord":
        payload = _format_discord_payload(level, message, details)
    elif webhook_type == "slack":
        payload = _format_slack_payload(level, message, details)
    else:
        payload = _format_generic_payload(level, message, details)
    
    # Send the alert
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                ALERT_WEBHOOK_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code < 300:
                logger.info(f"Alert sent: {level.value} - {message[:50]}...")
                return True
            else:
                logger.warning(
                    f"Alert webhook returned {response.status_code}",
                    extra={"response": response.text[:200]}
                )
                return False
                
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")
        return False


def send_alert(
    level: AlertLevel,
    message: str,
    details: Optional[dict] = None,
    alert_key: Optional[str] = None
) -> bool:
    """
    Send an alert synchronously (creates event loop if needed).
    
    For use in non-async code. Prefer send_alert_async when possible.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # We're in an async context, schedule it
            asyncio.create_task(send_alert_async(level, message, details, alert_key))
            return True
        else:
            return loop.run_until_complete(
                send_alert_async(level, message, details, alert_key)
            )
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(send_alert_async(level, message, details, alert_key))


# ============================================
# Convenience Functions
# ============================================

def alert_error(message: str, **details) -> bool:
    """Send an error-level alert."""
    return send_alert(AlertLevel.ERROR, message, details if details else None)


def alert_critical(message: str, **details) -> bool:
    """Send a critical-level alert."""
    return send_alert(AlertLevel.CRITICAL, message, details if details else None)


async def alert_error_async(message: str, **details) -> bool:
    """Send an error-level alert asynchronously."""
    return await send_alert_async(AlertLevel.ERROR, message, details if details else None)


async def alert_critical_async(message: str, **details) -> bool:
    """Send a critical-level alert asynchronously."""
    return await send_alert_async(AlertLevel.CRITICAL, message, details if details else None)


# ============================================
# Logging Integration
# ============================================

class AlertHandler(logging.Handler):
    """
    Logging handler that sends alerts for ERROR and CRITICAL logs.
    
    Usage:
        import logging
        from utils.alerts import AlertHandler
        
        logger = logging.getLogger("orbital")
        logger.addHandler(AlertHandler())
    """
    
    def emit(self, record: logging.LogRecord):
        if record.levelno >= logging.CRITICAL:
            send_alert(AlertLevel.CRITICAL, record.getMessage())
        elif record.levelno >= logging.ERROR:
            send_alert(AlertLevel.ERROR, record.getMessage())
