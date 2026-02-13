"use client"

import { createContext, useContext, useEffect, useState, useCallback, useRef, ReactNode } from 'react'
import { User } from '@supabase/supabase-js'
import { getSupabase, resetSupabaseClient, Profile } from './supabase'

interface AuthContextType {
  user: User | null
  profile: Profile | null
  loading: boolean
  signUp: (email: string, password: string) => Promise<{ data: any; error: any }>
  signIn: (email: string, password: string) => Promise<{ data: any; error: any }>
  signOut: () => Promise<{ error: any }>
  refreshProfile: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const initializedRef = useRef(false)

  const fetchProfile = useCallback(async (userId: string, client: ReturnType<typeof getSupabase>) => {
    console.log('[Auth] fetchProfile starting for:', userId)
    try {
      const { data, error } = await client
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single()

      if (error && error.code !== 'PGRST116') {
        console.error('[Auth] Profile fetch error:', error.message)
      }
      
      if (data) {
        console.log('[Auth] Profile fetched successfully')
        setProfile(data as Profile)
      } else {
        console.log('[Auth] No profile data returned')
      }
    } catch (err) {
      console.error('[Auth] Profile fetch error:', err)
    }
  }, [])

  useEffect(() => {
    if (initializedRef.current) return
    initializedRef.current = true

    let mounted = true
    let authEventReceived = false  // Use local variable, not state

    // Check if returning from Stripe
    const urlParams = new URLSearchParams(window.location.search)
    const fromStripe = urlParams.has('success') || urlParams.has('canceled')
    
    // Reset client if coming from Stripe
    const supabase = fromStripe ? resetSupabaseClient() : getSupabase()
    console.log('[Auth] Init, fromStripe:', fromStripe)

    // Listen for auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        if (!mounted) return
        
        authEventReceived = true  // Mark that we received an event
        console.log('[Auth] Auth state changed:', event, session?.user?.email)

        // Handle all events that indicate auth state
        if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
          if (session?.user) {
            console.log('[Auth] Setting user:', session.user.email)
            setUser(session.user)
            // Set loading false IMMEDIATELY - don't wait for profile
            setLoading(false)
            // Fetch profile in background (fire and forget)
            fetchProfile(session.user.id, supabase)
          } else {
            console.log('[Auth] No user in session')
            setUser(null)
            setProfile(null)
            setLoading(false)
          }
        }

        if (event === 'SIGNED_OUT') {
          console.log('[Auth] User signed out')
          setUser(null)
          setProfile(null)
          setLoading(false)
        }
      }
    )

    // Safety timeout - only fires if NO auth event was received
    const timeout = setTimeout(() => {
      if (mounted && !authEventReceived) {
        console.warn('[Auth] No auth event received in 5s, assuming not logged in')
        setUser(null)
        setProfile(null)
        setLoading(false)
      }
    }, 5000)

    return () => {
      mounted = false
      clearTimeout(timeout)
      subscription.unsubscribe()
    }
  }, [fetchProfile])

  const signUp = async (email: string, password: string) => {
    const supabase = getSupabase()
    const { data, error } = await supabase.auth.signUp({ email, password })
    return { data, error }
  }

  const signIn = async (email: string, password: string) => {
    const supabase = getSupabase()
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    return { data, error }
  }

  const signOut = async () => {
    const supabase = getSupabase()
    const { error } = await supabase.auth.signOut()
    if (error) {
      console.error('[Auth] SignOut error:', error.message)
    }
    return { error }
  }

  const refreshProfile = async () => {
    if (user) {
      const supabase = getSupabase()
      await fetchProfile(user.id, supabase)
    }
  }

  return (
    <AuthContext.Provider value={{
      user,
      profile,
      loading,
      signUp,
      signIn,
      signOut,
      refreshProfile,
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
