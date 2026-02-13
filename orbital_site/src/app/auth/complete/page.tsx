"use client"

import { useEffect, useState, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { getSupabase } from '@/lib/supabase'

// Fallback page for completing OAuth when hash fragments are involved
// Route: /auth/complete (redirect here from callback if needed)

function AuthCompleteContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [status, setStatus] = useState('Completing authentication...')
  const supabase = getSupabase()

  useEffect(() => {
    const complete = async () => {
      // Check for error in query params first
      const error = searchParams.get('error')
      if (error) {
        setStatus(`Error: ${error}`)
        setTimeout(() => router.push(`/login?error=${error}`), 2000)
        return
      }

      try {
        // First check if there's a hash fragment with tokens (implicit flow fallback)
        if (window.location.hash.includes('access_token')) {
          setStatus('Processing session from URL...')
          
          // The Supabase client auto-detects hash fragments on init
          // Give it a moment to process
          await new Promise(r => setTimeout(r, 300))
        }

        // Verify we have a valid user
        const { data: { user }, error: authError } = await supabase.auth.getUser()
        
        if (authError) {
          console.error('Auth verification error:', authError)
          setStatus(`Error: ${authError.message}`)
          setTimeout(() => router.push('/login?error=verification_failed'), 2000)
          return
        }

        if (user) {
          setStatus(`Welcome, ${user.email}! Redirecting...`)
          // Clear any hash fragments
          if (window.location.hash) {
            window.history.replaceState(null, '', '/auth/complete')
          }
          router.push('/dashboard')
        } else {
          setStatus('No session found, redirecting to login...')
          setTimeout(() => router.push('/login'), 2000)
        }
        
      } catch (err) {
        console.error('Complete auth error:', err)
        setStatus('Authentication failed')
        setTimeout(() => router.push('/login?error=complete_failed'), 2000)
      }
    }

    complete()
  }, [router, supabase, searchParams])

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="text-center">
        <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-white/70 text-sm">{status}</p>
      </div>
    </div>
  )
}

export default function AuthCompletePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
      </div>
    }>
      <AuthCompleteContent />
    </Suspense>
  )
}
