"""
Orbital Payment Routes
Uses Stripe for payments
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Header
from pydantic import BaseModel
from typing import Optional
import os
import stripe
from supabase import create_client, Client

router = APIRouter(prefix="/payments", tags=["payments"])

# Stripe setup
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

# Pricing tiers
TIERS = {
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
    success_url: str
    cancel_url: str

class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str

# ============================================
# Auth dependency (copied from auth.py)
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
    """Create Stripe checkout session for minute purchase"""
    
    if request.tier not in TIERS:
        raise HTTPException(status_code=400, detail=f"Invalid tier. Must be one of: {list(TIERS.keys())}")
    
    tier = TIERS[request.tier]
    
    if not tier["price_id"]:
        raise HTTPException(status_code=500, detail="Stripe prices not configured")
    
    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": tier["price_id"],
                "quantity": 1
            }],
            mode="payment",
            success_url=request.success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.cancel_url,
            client_reference_id=user.id,  # To identify user in webhook
            metadata={
                "user_id": user.id,
                "tier": request.tier,
                "minutes": tier["minutes"]
            }
        )
        
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
    
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        user_id = session.get("client_reference_id") or session["metadata"].get("user_id")
        tier_name = session["metadata"].get("tier")
        minutes = float(session["metadata"].get("minutes", 0))
        amount_cents = session["amount_total"]
        
        if user_id and minutes > 0:
            # Add minutes to user's balance
            supabase = get_supabase_admin()
            
            try:
                # Call the add_minutes function
                result = supabase.rpc("add_minutes", {
                    "p_user_id": user_id,
                    "p_minutes": minutes,
                    "p_amount_cents": amount_cents,
                    "p_tier": tier_name,
                    "p_stripe_session_id": session["id"]
                }).execute()
                
                print(f"✅ Added {minutes} minutes to user {user_id}")
                
            except Exception as e:
                print(f"❌ Failed to add minutes: {e}")
                # Don't raise - Stripe will retry. Log for manual resolution.
    
    return {"received": True}

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
