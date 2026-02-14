"""
Minutes Management
==================
Safe, atomic operations for crediting and debiting user minutes.

All operations:
- Use PostgreSQL transactions with row locking
- Are idempotent (same reference_id = same result)
- Create audit trail in minute_transactions table

Usage:
    from utils.minutes import credit_minutes, debit_minutes, get_balance

    # Credit minutes (e.g., from Stripe webhook)
    result = await credit_minutes(
        user_id="uuid",
        amount=10.0,
        source="stripe",
        reference_id="cs_xxx"  # Stripe session ID for idempotency
    )

    # Debit minutes (e.g., after video generation)
    result = await debit_minutes(
        user_id="uuid",
        amount=2.5,
        source="job_complete",
        reference_id="job_abc123"  # Job ID for idempotency
    )
"""

import os
from typing import Optional
from dataclasses import dataclass

from supabase import create_client, Client

from utils.logging import logger, log_error
from utils.alerts import alert_error


# ============================================
# Result Types
# ============================================

@dataclass
class MinutesResult:
    """Result of a credit/debit operation."""
    success: bool
    transaction_id: Optional[str] = None
    previous_balance: Optional[float] = None
    amount: Optional[float] = None
    new_balance: Optional[float] = None
    error: Optional[str] = None
    idempotent: bool = False  # True if this was a duplicate request


@dataclass
class BalanceResult:
    """Result of a balance check."""
    success: bool
    balance: Optional[float] = None
    error: Optional[str] = None


# ============================================
# Supabase Client
# ============================================

_supabase_admin: Optional[Client] = None


def get_supabase_admin() -> Client:
    """Get Supabase client with service role (admin) privileges."""
    global _supabase_admin
    
    if _supabase_admin is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY required")
        
        _supabase_admin = create_client(url, key)
    
    return _supabase_admin


# ============================================
# Core Operations
# ============================================

async def credit_minutes(
    user_id: str,
    amount: float,
    source: str,
    reference_id: Optional[str] = None,
    metadata: Optional[dict] = None
) -> MinutesResult:
    """
    Credit minutes to a user's balance.
    
    Args:
        user_id: UUID of the user
        amount: Minutes to add (must be positive)
        source: Where the credit came from ('stripe', 'admin', 'signup_bonus', etc.)
        reference_id: Unique ID for idempotency (e.g., Stripe session ID)
        metadata: Optional extra context (stored as JSONB)
    
    Returns:
        MinutesResult with success status and new balance
    
    Security:
        - Idempotent: Same reference_id returns same result (no double-credit)
        - Atomic: Uses PostgreSQL transaction
        - Audited: Creates record in minute_transactions
    """
    if amount <= 0:
        return MinutesResult(success=False, error="Amount must be positive")
    
    try:
        supabase = get_supabase_admin()
        
        result = supabase.rpc("credit_minutes_safe", {
            "p_user_id": user_id,
            "p_amount": amount,
            "p_source": source,
            "p_reference_id": reference_id,
            "p_metadata": metadata or {}
        }).execute()
        
        data = result.data
        
        if not data:
            return MinutesResult(success=False, error="No response from database")
        
        if data.get("success"):
            logger.info(
                f"Credited {amount} minutes to user",
                extra={
                    "event": "minutes_credit",
                    "user_id_partial": user_id[:8] + "...",
                    "amount": amount,
                    "source": source,
                    "new_balance": data.get("new_balance"),
                    "idempotent": data.get("idempotent", False)
                }
            )
            
            return MinutesResult(
                success=True,
                transaction_id=data.get("transaction_id"),
                previous_balance=data.get("previous_balance"),
                amount=amount,
                new_balance=data.get("new_balance"),
                idempotent=data.get("idempotent", False)
            )
        else:
            return MinutesResult(
                success=False,
                error=data.get("error", "Unknown error")
            )
            
    except Exception as e:
        log_error(f"Failed to credit minutes", error=e, user_id=user_id[:8], amount=amount)
        alert_error("Minutes credit failed", source=source, error=str(e)[:200])
        return MinutesResult(success=False, error=str(e))


async def debit_minutes(
    user_id: str,
    amount: float,
    source: str,
    reference_id: Optional[str] = None,
    metadata: Optional[dict] = None
) -> MinutesResult:
    """
    Debit minutes from a user's balance.
    
    Args:
        user_id: UUID of the user
        amount: Minutes to deduct (must be positive)
        source: Why the debit happened ('job_complete', 'admin', etc.)
        reference_id: Unique ID for idempotency (e.g., job ID)
        metadata: Optional extra context (stored as JSONB)
    
    Returns:
        MinutesResult with success status and new balance
    
    Security:
        - Checks sufficient balance before deducting
        - Idempotent: Same reference_id returns same result (no double-debit)
        - Atomic: Uses PostgreSQL transaction with row locking
        - Audited: Creates record in minute_transactions
    """
    if amount <= 0:
        return MinutesResult(success=False, error="Amount must be positive")
    
    try:
        supabase = get_supabase_admin()
        
        result = supabase.rpc("debit_minutes_safe", {
            "p_user_id": user_id,
            "p_amount": amount,
            "p_source": source,
            "p_reference_id": reference_id,
            "p_metadata": metadata or {}
        }).execute()
        
        data = result.data
        
        if not data:
            return MinutesResult(success=False, error="No response from database")
        
        if data.get("success"):
            logger.info(
                f"Debited {amount} minutes from user",
                extra={
                    "event": "minutes_debit",
                    "user_id_partial": user_id[:8] + "...",
                    "amount": amount,
                    "source": source,
                    "new_balance": data.get("new_balance"),
                    "idempotent": data.get("idempotent", False)
                }
            )
            
            return MinutesResult(
                success=True,
                transaction_id=data.get("transaction_id"),
                previous_balance=data.get("previous_balance"),
                amount=amount,
                new_balance=data.get("new_balance"),
                idempotent=data.get("idempotent", False)
            )
        else:
            # Log insufficient balance as info (not error - expected case)
            if "insufficient" in data.get("error", "").lower():
                logger.info(
                    f"Insufficient balance for debit",
                    extra={
                        "event": "minutes_debit_insufficient",
                        "user_id_partial": user_id[:8] + "...",
                        "requested": amount,
                        "current_balance": data.get("current_balance")
                    }
                )
            
            return MinutesResult(
                success=False,
                error=data.get("error", "Unknown error")
            )
            
    except Exception as e:
        log_error(f"Failed to debit minutes", error=e, user_id=user_id[:8], amount=amount)
        alert_error("Minutes debit failed", source=source, error=str(e)[:200])
        return MinutesResult(success=False, error=str(e))


async def get_balance(user_id: str) -> BalanceResult:
    """
    Get current minutes balance for a user.
    
    Args:
        user_id: UUID of the user
    
    Returns:
        BalanceResult with current balance
    """
    try:
        supabase = get_supabase_admin()
        
        result = supabase.table("profiles") \
            .select("minutes_balance") \
            .eq("id", user_id) \
            .single() \
            .execute()
        
        if result.data:
            return BalanceResult(
                success=True,
                balance=float(result.data.get("minutes_balance", 0))
            )
        else:
            return BalanceResult(success=False, error="User not found")
            
    except Exception as e:
        return BalanceResult(success=False, error=str(e))


async def get_transactions(
    user_id: str,
    limit: int = 50
) -> list[dict]:
    """
    Get transaction history for a user.
    
    Args:
        user_id: UUID of the user
        limit: Maximum number of transactions to return
    
    Returns:
        List of transaction records (most recent first)
    """
    try:
        supabase = get_supabase_admin()
        
        result = supabase.rpc("get_minute_transactions", {
            "p_user_id": user_id,
            "p_limit": limit
        }).execute()
        
        return result.data or []
        
    except Exception as e:
        log_error(f"Failed to get transactions", error=e, user_id=user_id[:8])
        return []


# ============================================
# Sync Wrappers (for non-async code)
# ============================================

def credit_minutes_sync(
    user_id: str,
    amount: float,
    source: str,
    reference_id: Optional[str] = None,
    metadata: Optional[dict] = None
) -> MinutesResult:
    """Synchronous wrapper for credit_minutes."""
    import asyncio
    return asyncio.get_event_loop().run_until_complete(
        credit_minutes(user_id, amount, source, reference_id, metadata)
    )


def debit_minutes_sync(
    user_id: str,
    amount: float,
    source: str,
    reference_id: Optional[str] = None,
    metadata: Optional[dict] = None
) -> MinutesResult:
    """Synchronous wrapper for debit_minutes."""
    import asyncio
    return asyncio.get_event_loop().run_until_complete(
        debit_minutes(user_id, amount, source, reference_id, metadata)
    )
