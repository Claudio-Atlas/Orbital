// Supabase client - using SSR client (cookies) as per industry standard
// Note: We had issues with getSession() hanging after Stripe redirect
// This file includes debugging to identify the root cause

import { createBrowserClient } from '@supabase/ssr'

// Types for our database
export type Profile = {
  id: string
  email: string
  display_name: string | null
  minutes_balance: number
  created_at: string
  updated_at: string
}

export type Purchase = {
  id: string
  user_id: string
  minutes: number
  amount_cents: number
  stripe_payment_id: string | null
  tier: 'starter' | 'standard' | 'pro'
  created_at: string
}

export type Video = {
  id: string
  user_id: string
  problem: string
  problem_type: 'latex' | 'text'
  video_url: string | null
  thumbnail_url: string | null
  minutes_used: number
  voice_id: string
  status: 'pending' | 'processing' | 'complete' | 'error'
  expires_at: string
  created_at: string
}

// Create Supabase browser client (SSR - uses cookies)
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// Singleton for client-side usage
let supabaseClient: ReturnType<typeof createClient> | null = null

export function getSupabase() {
  if (typeof window === 'undefined') {
    // Server-side: always create a new client
    return createClient()
  }
  
  if (!supabaseClient) {
    console.log('[Supabase] Creating new browser client')
    supabaseClient = createClient()
  }
  return supabaseClient
}

// Force recreate client (call this after external navigation if needed)
export function resetSupabaseClient() {
  console.log('[Supabase] Resetting client')
  supabaseClient = null
  return getSupabase()
}
