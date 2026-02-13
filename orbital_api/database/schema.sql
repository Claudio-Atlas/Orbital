-- ORBITAL DATABASE SCHEMA
-- Supabase Postgres
-- Run this in Supabase SQL Editor

-- ============================================
-- USERS TABLE (extends Supabase auth.users)
-- ============================================
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    minutes_balance DECIMAL(10,2) DEFAULT 0,
    total_minutes_purchased DECIMAL(10,2) DEFAULT 0,
    total_spent_cents INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Users can only read/update their own profile
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- ============================================
-- PURCHASES TABLE
-- ============================================
CREATE TABLE public.purchases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    -- Purchase details
    tier TEXT NOT NULL, -- 'starter', 'standard', 'pro'
    minutes_added DECIMAL(10,2) NOT NULL,
    amount_cents INTEGER NOT NULL, -- Price in cents ($2 = 200)
    
    -- Stripe
    stripe_payment_intent_id TEXT,
    stripe_checkout_session_id TEXT UNIQUE, -- Unique for idempotency
    
    -- Status
    status TEXT DEFAULT 'completed', -- 'pending', 'completed', 'refunded'
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.purchases ENABLE ROW LEVEL SECURITY;

-- Users can only view their own purchases
CREATE POLICY "Users can view own purchases" ON public.purchases
    FOR SELECT USING (auth.uid() = user_id);

-- Index for user lookups
CREATE INDEX idx_purchases_user_id ON public.purchases(user_id);

-- ============================================
-- VIDEOS TABLE
-- ============================================
CREATE TABLE public.videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    
    -- Problem
    problem_text TEXT NOT NULL,
    problem_type TEXT, -- 'algebra', 'calculus', 'geometry', etc.
    
    -- Generation
    minutes_used DECIMAL(10,2) NOT NULL,
    character_count INTEGER NOT NULL,
    steps_count INTEGER,
    
    -- Storage
    video_url TEXT, -- R2 URL
    video_key TEXT, -- R2 object key for deletion
    thumbnail_url TEXT,
    
    -- Status
    status TEXT DEFAULT 'generating', -- 'generating', 'complete', 'failed', 'expired'
    error_message TEXT,
    
    -- Expiry
    expires_at TIMESTAMPTZ NOT NULL, -- NOW() + 48 hours
    
    -- Email
    emailed BOOLEAN DEFAULT FALSE,
    emailed_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.videos ENABLE ROW LEVEL SECURITY;

-- Users can only view their own videos
CREATE POLICY "Users can view own videos" ON public.videos
    FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own videos
CREATE POLICY "Users can insert own videos" ON public.videos
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Indexes
CREATE INDEX idx_videos_user_id ON public.videos(user_id);
CREATE INDEX idx_videos_expires_at ON public.videos(expires_at);
CREATE INDEX idx_videos_status ON public.videos(status);

-- ============================================
-- FUNCTIONS
-- ============================================

-- Function to create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email)
    VALUES (NEW.id, NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users insert
CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function to deduct minutes (called from API)
CREATE OR REPLACE FUNCTION public.deduct_minutes(
    p_user_id UUID,
    p_minutes DECIMAL
)
RETURNS BOOLEAN AS $$
DECLARE
    v_balance DECIMAL;
BEGIN
    -- Get current balance
    SELECT minutes_balance INTO v_balance
    FROM public.profiles
    WHERE id = p_user_id
    FOR UPDATE; -- Lock row
    
    -- Check sufficient balance
    IF v_balance < p_minutes THEN
        RETURN FALSE;
    END IF;
    
    -- Deduct
    UPDATE public.profiles
    SET minutes_balance = minutes_balance - p_minutes,
        updated_at = NOW()
    WHERE id = p_user_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to add minutes after purchase (IDEMPOTENT)
-- Returns existing purchase ID if already processed (safe to retry)
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
    
    -- If already processed, return existing ID (don't duplicate)
    IF v_existing_id IS NOT NULL THEN
        RETURN v_existing_id;
    END IF;

    -- Add to balance
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
-- PRICING CONSTANTS (for reference)
-- ============================================
-- Starter: $2 (200 cents) = 10 minutes
-- Standard: $8 (800 cents) = 50 minutes  
-- Pro: $15 (1500 cents) = 120 minutes
--
-- Cost to us: ~$0.016/minute
-- Margins: 87-92%
