"""
Orbital Payment Routes
Uses Stripe for one-time and subscription payments
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Header
from pydantic import BaseModel
from typing import Optional, Literal
import os
import stripe
from supabase import create_client, Client

from utils.logging import logger, log_error
from utils.alerts import alert_error, alert_critical
from utils.minutes import credit_minutes_sync

router = APIRouter(prefix="/payments", tags=["payments"])

# Stripe setup
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

# Pricing tiers - One-time prices
TIERS_ONETIME = {
    "starter": {
        "price_id": os.environ.get("STRIPE_PRICE_STARTER"),
        "minutes": 10,
        "amount_cents": 200  # $2
    },
    "standard": {
        "price_id": os.environ.get("STRIPE_PRICE_STANDARD"),
        "minutes": 50,
        "amount_cents": 800  # $8
    },
    "pro": {
        "price_id": os.environ.get("STRIPE_PRICE_PRO"),
        "minutes": 120,
        "amount_cents": 1500  # $15
    }
}

# Pricing tiers - Subscription prices
TIERS_SUBSCRIPTION = {
    "starter": {
        "price_id": os.environ.get("STRIPE_PRICE_STARTER_SUB"),
        "minutes": 10,
        "amount_cents": 150  # $1.50/mo
    },
    "standard": {
        "price_id": os.environ.get("STRIPE_PRICE_STANDARD_SUB"),
        "minutes": 50,
        "amount_cents": 600  # $6/mo
    },
    "pro": {
        "price_id": os.environ.get("STRIPE_PRICE_PRO_SUB"),
        "minutes": 120,
        "amount_cents": 1200  # $12/mo
    }
}

# Supabase client
def get_supabase_admin() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    return create_client(url, key)

# ============================================
# Models
# ============================================

class CreateCheckoutRequest(BaseModel):
    tier: str  # 'starter', 'standard', 'pro'
    mode: Literal["payment", "subscription"] = "payment"  # one-time or subscription
    success_url: str
    cancel_url: str

class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str

class SubscriptionStatus(BaseModel):
    active: bool
    tier: Optional[str] = None
    current_period_end: Optional[str] = None
    cancel_at_period_end: bool = False

# ============================================
# Auth dependency
# ============================================

async def get_current_user(authorization: str = Header(...)):
    """Verify JWT and return user"""
    from supabase import create_client
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    supabase = create_client(url, key)
    
    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# ============================================
# Routes
# ============================================

@router.post("/create-checkout", response_model=CheckoutResponse)
async def create_checkout(request: CreateCheckoutRequest, user = Depends(get_current_user)):
    """Create Stripe checkout session for minute purchase or subscription"""
    
    # Select the right tier dict based on mode
    tiers = TIERS_SUBSCRIPTION if request.mode == "subscription" else TIERS_ONETIME
    
    if request.tier not in tiers:
        raise HTTPException(status_code=400, detail=f"Invalid tier. Must be one of: {list(tiers.keys())}")
    
    tier = tiers[request.tier]
    
    if not tier["price_id"]:
        raise HTTPException(status_code=500, detail="Stripe prices not configured")
    
    try:
        # Check if user already has a subscription (for subscription mode)
        if request.mode == "subscription":
            supabase = get_supabase_admin()
            profile = supabase.table("profiles").select("stripe_customer_id, subscription_tier").eq("id", user.id).single().execute()
            
            if profile.data and profile.data.get("subscription_tier"):
                raise HTTPException(
                    status_code=400, 
                    detail="You already have an active subscription. Cancel first to change plans."
                )
        
        # Create Stripe checkout session
        session_params = {
            "payment_method_types": ["card"],
            "line_items": [{
                "price": tier["price_id"],
                "quantity": 1
            }],
            "mode": request.mode,
            "success_url": request.success_url + "?session_id={CHECKOUT_SESSION_ID}",
            "cancel_url": request.cancel_url,
            "client_reference_id": user.id,
            "metadata": {
                "user_id": user.id,
                "tier": request.tier,
                "minutes": tier["minutes"],
                "mode": request.mode
            }
        }
        
        # For subscriptions, allow promotion codes
        if request.mode == "subscription":
            session_params["allow_promotion_codes"] = True
        
        session = stripe.checkout.Session.create(**session_params)
        
        return CheckoutResponse(
            checkout_url=session.url,
            session_id=session.id
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    # SECURITY: Webhook signature verification is REQUIRED
    # Never process webhooks without verifying they came from Stripe
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500, 
            detail="Webhook secret not configured. Cannot process webhooks securely."
        )
    
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    supabase = get_supabase_admin()
    
    # Handle checkout.session.completed (both one-time and first subscription payment)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        user_id = session.get("client_reference_id") or session["metadata"].get("user_id")
        tier_name = session["metadata"].get("tier")
        minutes = float(session["metadata"].get("minutes", 0))
        mode = session["metadata"].get("mode", "payment")
        amount_cents = session["amount_total"]
        
        if user_id and minutes > 0:
            try:
                # Credit minutes using safe, atomic function
                result = credit_minutes_sync(
                    user_id=user_id,
                    amount=minutes,
                    source="stripe",
                    reference_id=session["id"],  # Idempotency: same session = same credit
                    metadata={
                        "tier": tier_name,
                        "amount_cents": amount_cents,
                        "mode": mode
                    }
                )
                
                if result.success:
                    if result.idempotent:
                        logger.info(f"Idempotent: Already credited {minutes} minutes for session {session['id'][:20]}")
                    else:
                        logger.info(f"✅ Credited {minutes} minutes to user {user_id[:8]}... (new balance: {result.new_balance})")
                else:
                    log_error(f"Failed to credit minutes: {result.error}", user_id=user_id[:8])
                    alert_critical("Stripe webhook: Failed to credit minutes", 
                                 session_id=session["id"][:20], error=result.error)
                
                # If subscription, store the subscription info
                if mode == "subscription" and session.get("subscription"):
                    supabase.table("profiles").update({
                        "stripe_customer_id": session.get("customer"),
                        "stripe_subscription_id": session.get("subscription"),
                        "subscription_tier": tier_name
                    }).eq("id", user_id).execute()
                    
                    logger.info(f"✅ Updated subscription info for user {user_id[:8]}...")
                
            except Exception as e:
                log_error(f"Failed to process checkout", error=e, session_id=session["id"][:20])
                alert_critical("Stripe webhook processing failed", error=str(e)[:200])
    
    # Handle subscription renewal (invoice.paid for recurring payments)
    elif event["type"] == "invoice.paid":
        invoice = event["data"]["object"]
        
        # Skip if this is the first invoice (already handled by checkout.session.completed)
        if invoice.get("billing_reason") == "subscription_create":
            return {"received": True}
        
        subscription_id = invoice.get("subscription")
        customer_id = invoice.get("customer")
        
        if subscription_id:
            try:
                # Find user by subscription ID
                profile = supabase.table("profiles") \
                    .select("id, subscription_tier") \
                    .eq("stripe_subscription_id", subscription_id) \
                    .single() \
                    .execute()
                
                if profile.data:
                    user_id = profile.data["id"]
                    tier_name = profile.data.get("subscription_tier", "starter")
                    tier = TIERS_SUBSCRIPTION.get(tier_name, TIERS_SUBSCRIPTION["starter"])
                    minutes = tier["minutes"]
                    amount_cents = invoice.get("amount_paid", tier["amount_cents"])
                    
                    # Credit monthly minutes using safe, atomic function
                    result = credit_minutes_sync(
                        user_id=user_id,
                        amount=minutes,
                        source="stripe_renewal",
                        reference_id=invoice["id"],  # Idempotency
                        metadata={
                            "tier": tier_name,
                            "amount_cents": amount_cents,
                            "billing_reason": invoice.get("billing_reason")
                        }
                    )
                    
                    if result.success:
                        logger.info(f"✅ Monthly renewal: Credited {minutes} minutes to user {user_id[:8]}...")
                    else:
                        log_error(f"Failed to credit renewal minutes: {result.error}", user_id=user_id[:8])
                        alert_critical("Subscription renewal: Failed to credit minutes",
                                     invoice_id=invoice["id"][:20], error=result.error)
                    
            except Exception as e:
                log_error(f"Failed to process renewal", error=e, invoice_id=invoice.get("id", "?")[:20])
                alert_critical("Subscription renewal processing failed", error=str(e)[:200])
    
    # Handle subscription cancellation
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        subscription_id = subscription.get("id")
        
        if subscription_id:
            try:
                supabase.table("profiles").update({
                    "stripe_subscription_id": None,
                    "subscription_tier": None
                }).eq("stripe_subscription_id", subscription_id).execute()
                
                print(f"✅ Subscription {subscription_id} cancelled")
                
            except Exception as e:
                print(f"❌ Failed to process cancellation: {e}")
    
    return {"received": True}

@router.post("/cancel-subscription")
async def cancel_subscription(user = Depends(get_current_user)):
    """Cancel user's subscription at end of billing period"""
    
    supabase = get_supabase_admin()
    
    try:
        profile = supabase.table("profiles") \
            .select("stripe_subscription_id") \
            .eq("id", user.id) \
            .single() \
            .execute()
        
        subscription_id = profile.data.get("stripe_subscription_id") if profile.data else None
        
        if not subscription_id:
            raise HTTPException(status_code=400, detail="No active subscription")
        
        # Cancel at period end (user keeps access until then)
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        
        return {"message": "Subscription will cancel at end of billing period"}
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subscription-status", response_model=SubscriptionStatus)
async def get_subscription_status(user = Depends(get_current_user)):
    """Get user's subscription status"""
    
    supabase = get_supabase_admin()
    
    try:
        profile = supabase.table("profiles") \
            .select("stripe_subscription_id, subscription_tier") \
            .eq("id", user.id) \
            .single() \
            .execute()
        
        subscription_id = profile.data.get("stripe_subscription_id") if profile.data else None
        
        if not subscription_id:
            return SubscriptionStatus(active=False)
        
        # Get subscription details from Stripe
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        return SubscriptionStatus(
            active=subscription.status == "active",
            tier=profile.data.get("subscription_tier"),
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end
        )
        
    except stripe.error.StripeError:
        return SubscriptionStatus(active=False)

@router.get("/history")
async def get_purchase_history(user = Depends(get_current_user)):
    """Get user's purchase history"""
    
    supabase = get_supabase_admin()
    
    try:
        result = supabase.table("purchases") \
            .select("*") \
            .eq("user_id", user.id) \
            .order("created_at", desc=True) \
            .limit(50) \
            .execute()
        
        return {
            "purchases": result.data or []
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/balance")
async def get_balance(user = Depends(get_current_user)):
    """Get current minutes balance"""
    
    supabase = get_supabase_admin()
    
    try:
        result = supabase.table("profiles") \
            .select("minutes_balance") \
            .eq("id", user.id) \
            .single() \
            .execute()
        
        return {
            "minutes_balance": float(result.data.get("minutes_balance", 0)) if result.data else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/prices")
async def get_prices():
    """Get all available prices (for frontend pricing display)"""
    
    return {
        "one_time": {
            tier: {
                "minutes": data["minutes"],
                "amount_cents": data["amount_cents"],
                "price_per_minute": round(data["amount_cents"] / data["minutes"] / 100, 2)
            }
            for tier, data in TIERS_ONETIME.items()
        },
        "subscription": {
            tier: {
                "minutes": data["minutes"],
                "amount_cents": data["amount_cents"],
                "price_per_minute": round(data["amount_cents"] / data["minutes"] / 100, 2)
            }
            for tier, data in TIERS_SUBSCRIPTION.items()
        }
    }
