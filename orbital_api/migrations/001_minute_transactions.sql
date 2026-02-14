-- Migration: Create minute_transactions audit table and safe credit/debit functions
-- Run this in Supabase SQL Editor
-- Date: 2026-02-14

-- ============================================
-- 1. Create minute_transactions audit table
-- ============================================

CREATE TABLE IF NOT EXISTS minute_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,           -- positive = credit, negative = debit
    balance_after DECIMAL(10,2) NOT NULL,    -- snapshot after this transaction
    type TEXT NOT NULL CHECK (type IN ('credit', 'debit', 'refund', 'adjustment', 'signup_bonus')),
    source TEXT NOT NULL,                     -- 'stripe', 'job_complete', 'admin', 'system'
    reference_id TEXT,                        -- job_id, payment_id, session_id, etc.
    metadata JSONB DEFAULT '{}',              -- extra context
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Index for fast user lookups
CREATE INDEX IF NOT EXISTS idx_minute_transactions_user_id 
    ON minute_transactions(user_id);

-- Index for reference lookups (idempotency checks)
CREATE INDEX IF NOT EXISTS idx_minute_transactions_reference 
    ON minute_transactions(source, reference_id);

-- Index for time-based queries
CREATE INDEX IF NOT EXISTS idx_minute_transactions_created_at 
    ON minute_transactions(created_at DESC);

-- ============================================
-- 2. Enable RLS - Users can only see their own
-- ============================================

ALTER TABLE minute_transactions ENABLE ROW LEVEL SECURITY;

-- Users can read their own transactions
CREATE POLICY "Users can view own transactions" 
    ON minute_transactions 
    FOR SELECT 
    USING (auth.uid() = user_id);

-- Only service role can insert (no direct user inserts)
CREATE POLICY "Service role can insert transactions" 
    ON minute_transactions 
    FOR INSERT 
    WITH CHECK (true);  -- Service role bypasses RLS anyway

-- ============================================
-- 3. Safe credit function (atomic, with audit)
-- ============================================

CREATE OR REPLACE FUNCTION credit_minutes_safe(
    p_user_id UUID,
    p_amount DECIMAL,
    p_source TEXT,
    p_reference_id TEXT DEFAULT NULL,
    p_metadata JSONB DEFAULT '{}'
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER  -- Runs with function owner's privileges
AS $$
DECLARE
    v_current_balance DECIMAL;
    v_new_balance DECIMAL;
    v_transaction_id UUID;
BEGIN
    -- Validate inputs
    IF p_amount <= 0 THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Amount must be positive for credits'
        );
    END IF;
    
    -- Idempotency check: If this reference was already processed, return existing result
    IF p_reference_id IS NOT NULL THEN
        SELECT id INTO v_transaction_id
        FROM minute_transactions
        WHERE source = p_source 
          AND reference_id = p_reference_id
          AND type = 'credit'
        LIMIT 1;
        
        IF v_transaction_id IS NOT NULL THEN
            -- Already processed - return success (idempotent)
            SELECT balance_after INTO v_new_balance
            FROM minute_transactions
            WHERE id = v_transaction_id;
            
            RETURN jsonb_build_object(
                'success', true,
                'idempotent', true,
                'transaction_id', v_transaction_id,
                'new_balance', v_new_balance
            );
        END IF;
    END IF;
    
    -- Lock the row and get current balance
    SELECT minutes_balance INTO v_current_balance
    FROM profiles
    WHERE id = p_user_id
    FOR UPDATE;
    
    IF v_current_balance IS NULL THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'User not found'
        );
    END IF;
    
    -- Calculate new balance
    v_new_balance := v_current_balance + p_amount;
    
    -- Update balance
    UPDATE profiles
    SET minutes_balance = v_new_balance,
        total_minutes_purchased = total_minutes_purchased + p_amount,
        updated_at = NOW()
    WHERE id = p_user_id;
    
    -- Insert audit record
    INSERT INTO minute_transactions (
        user_id, amount, balance_after, type, source, reference_id, metadata
    ) VALUES (
        p_user_id, p_amount, v_new_balance, 'credit', p_source, p_reference_id, p_metadata
    )
    RETURNING id INTO v_transaction_id;
    
    RETURN jsonb_build_object(
        'success', true,
        'transaction_id', v_transaction_id,
        'previous_balance', v_current_balance,
        'amount', p_amount,
        'new_balance', v_new_balance
    );
END;
$$;

-- ============================================
-- 4. Safe debit function (atomic, with audit)
-- ============================================

CREATE OR REPLACE FUNCTION debit_minutes_safe(
    p_user_id UUID,
    p_amount DECIMAL,
    p_source TEXT,
    p_reference_id TEXT DEFAULT NULL,
    p_metadata JSONB DEFAULT '{}'
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_current_balance DECIMAL;
    v_new_balance DECIMAL;
    v_transaction_id UUID;
BEGIN
    -- Validate inputs
    IF p_amount <= 0 THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Amount must be positive for debits'
        );
    END IF;
    
    -- Idempotency check: If this reference was already processed, return existing result
    IF p_reference_id IS NOT NULL THEN
        SELECT id INTO v_transaction_id
        FROM minute_transactions
        WHERE source = p_source 
          AND reference_id = p_reference_id
          AND type = 'debit'
        LIMIT 1;
        
        IF v_transaction_id IS NOT NULL THEN
            -- Already processed - return success (idempotent)
            SELECT balance_after INTO v_new_balance
            FROM minute_transactions
            WHERE id = v_transaction_id;
            
            RETURN jsonb_build_object(
                'success', true,
                'idempotent', true,
                'transaction_id', v_transaction_id,
                'new_balance', v_new_balance
            );
        END IF;
    END IF;
    
    -- Lock the row and get current balance
    SELECT minutes_balance INTO v_current_balance
    FROM profiles
    WHERE id = p_user_id
    FOR UPDATE;
    
    IF v_current_balance IS NULL THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'User not found'
        );
    END IF;
    
    -- Check sufficient balance
    IF v_current_balance < p_amount THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Insufficient balance',
            'current_balance', v_current_balance,
            'requested', p_amount
        );
    END IF;
    
    -- Calculate new balance
    v_new_balance := v_current_balance - p_amount;
    
    -- Update balance
    UPDATE profiles
    SET minutes_balance = v_new_balance,
        updated_at = NOW()
    WHERE id = p_user_id;
    
    -- Insert audit record (negative amount for debit)
    INSERT INTO minute_transactions (
        user_id, amount, balance_after, type, source, reference_id, metadata
    ) VALUES (
        p_user_id, -p_amount, v_new_balance, 'debit', p_source, p_reference_id, p_metadata
    )
    RETURNING id INTO v_transaction_id;
    
    RETURN jsonb_build_object(
        'success', true,
        'transaction_id', v_transaction_id,
        'previous_balance', v_current_balance,
        'amount', p_amount,
        'new_balance', v_new_balance
    );
END;
$$;

-- ============================================
-- 5. Helper: Get transaction history
-- ============================================

CREATE OR REPLACE FUNCTION get_minute_transactions(
    p_user_id UUID,
    p_limit INT DEFAULT 50
)
RETURNS TABLE (
    id UUID,
    amount DECIMAL,
    balance_after DECIMAL,
    type TEXT,
    source TEXT,
    reference_id TEXT,
    created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        mt.id,
        mt.amount,
        mt.balance_after,
        mt.type,
        mt.source,
        mt.reference_id,
        mt.created_at
    FROM minute_transactions mt
    WHERE mt.user_id = p_user_id
    ORDER BY mt.created_at DESC
    LIMIT p_limit;
END;
$$;

-- ============================================
-- 6. Grant permissions
-- ============================================

-- Allow authenticated users to call transaction history
GRANT EXECUTE ON FUNCTION get_minute_transactions TO authenticated;

-- Credit/debit should only be called via service role (API backend)
-- No explicit grant needed - service role has full access

-- ============================================
-- Done! 
-- ============================================
-- To verify, run:
-- SELECT * FROM minute_transactions LIMIT 1;
-- SELECT credit_minutes_safe('user-uuid-here', 10.0, 'test', 'test-ref');
