-- MIGRATION: Add idempotency to prevent duplicate payment processing
-- Run this in Supabase SQL Editor
-- 
-- Problem: If Stripe webhook fires twice for the same checkout session,
-- the user gets double minutes. This migration prevents that.

-- ============================================
-- 1. Add unique constraint on stripe_checkout_session_id
-- ============================================

-- First, check for existing duplicates (just in case)
-- SELECT stripe_checkout_session_id, COUNT(*) 
-- FROM public.purchases 
-- WHERE stripe_checkout_session_id IS NOT NULL
-- GROUP BY stripe_checkout_session_id 
-- HAVING COUNT(*) > 1;

-- Add unique constraint (will fail if duplicates exist)
ALTER TABLE public.purchases 
ADD CONSTRAINT purchases_stripe_session_unique 
UNIQUE (stripe_checkout_session_id);

-- ============================================
-- 2. Update add_minutes to be idempotent
-- ============================================

CREATE OR REPLACE FUNCTION public.add_minutes(
    p_user_id UUID,
    p_minutes DECIMAL,
    p_amount_cents INTEGER,
    p_tier TEXT,
    p_stripe_session_id TEXT
)
RETURNS UUID AS $$
DECLARE
    v_purchase_id UUID;
    v_existing_id UUID;
BEGIN
    -- IDEMPOTENCY CHECK: See if this session was already processed
    SELECT id INTO v_existing_id
    FROM public.purchases
    WHERE stripe_checkout_session_id = p_stripe_session_id;
    
    -- If already processed, return the existing purchase ID (don't duplicate)
    IF v_existing_id IS NOT NULL THEN
        RETURN v_existing_id;
    END IF;

    -- Add to balance (with row lock to prevent race conditions)
    UPDATE public.profiles
    SET minutes_balance = minutes_balance + p_minutes,
        total_minutes_purchased = total_minutes_purchased + p_minutes,
        total_spent_cents = total_spent_cents + p_amount_cents,
        updated_at = NOW()
    WHERE id = p_user_id;
    
    -- Record purchase
    INSERT INTO public.purchases (user_id, tier, minutes_added, amount_cents, stripe_checkout_session_id)
    VALUES (p_user_id, p_tier, p_minutes, p_amount_cents, p_stripe_session_id)
    RETURNING id INTO v_purchase_id;
    
    RETURN v_purchase_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- VERIFICATION
-- ============================================
-- Test with:
-- SELECT public.add_minutes('your-user-uuid', 10, 200, 'starter', 'test-session-123');
-- Run again - should return same ID, not add more minutes
