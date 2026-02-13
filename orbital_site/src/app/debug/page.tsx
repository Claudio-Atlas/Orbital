"use client"

// Force dynamic rendering - uses Supabase client
export const dynamic = 'force-dynamic';

import { useState, useEffect } from 'react'
import { getSupabase } from '@/lib/supabase'

export default function DebugPage() {
  const [status, setStatus] = useState<string[]>([])
  const [cookies, setCookies] = useState<string>('')
  const supabase = getSupabase()

  const log = (msg: string) => {
    setStatus(prev => [...prev, `${new Date().toISOString().slice(11, 19)} - ${msg}`])
  }

  useEffect(() => {
    setCookies(document.cookie || '(none)')
  }, [])

  const checkAuth = async () => {
    log('Checking auth state...')
    
    try {
      log('Calling getUser()...')
      const start = Date.now()
      const { data: { user }, error } = await supabase.auth.getUser()
      const elapsed = Date.now() - start
      
      if (error) {
        log(`getUser() error (${elapsed}ms): ${error.message}`)
      } else if (user) {
        log(`getUser() success (${elapsed}ms): ${user.email}`)
      } else {
        log(`getUser() returned null (${elapsed}ms) - not logged in`)
      }
    } catch (e) {
      log(`getUser() threw: ${e}`)
    }

    try {
      log('Calling getSession()...')
      const start = Date.now()
      const { data: { session }, error } = await supabase.auth.getSession()
      const elapsed = Date.now() - start
      
      if (error) {
        log(`getSession() error (${elapsed}ms): ${error.message}`)
      } else if (session) {
        log(`getSession() success (${elapsed}ms): has token`)
      } else {
        log(`getSession() returned null (${elapsed}ms)`)
      }
    } catch (e) {
      log(`getSession() threw: ${e}`)
    }
  }

  const nukeEverything = async () => {
    log('🔥 NUKING ALL AUTH STATE...')
    
    // Sign out from Supabase
    try {
      await supabase.auth.signOut({ scope: 'global' })
      log('✓ Supabase signOut complete')
    } catch (e) {
      log(`✗ Supabase signOut failed: ${e}`)
    }
    
    // Clear localStorage
    try {
      const keys = Object.keys(localStorage)
      keys.forEach(key => {
        if (key.includes('supabase') || key.includes('sb-')) {
          localStorage.removeItem(key)
          log(`✓ Removed localStorage: ${key}`)
        }
      })
    } catch (e) {
      log(`✗ localStorage clear failed: ${e}`)
    }
    
    // Clear sessionStorage
    try {
      const keys = Object.keys(sessionStorage)
      keys.forEach(key => {
        if (key.includes('supabase') || key.includes('sb-')) {
          sessionStorage.removeItem(key)
          log(`✓ Removed sessionStorage: ${key}`)
        }
      })
    } catch (e) {
      log(`✗ sessionStorage clear failed: ${e}`)
    }
    
    // Clear cookies (as much as we can from JS)
    try {
      document.cookie.split(';').forEach(cookie => {
        const name = cookie.split('=')[0].trim()
        if (name.includes('supabase') || name.includes('sb-')) {
          document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`
          log(`✓ Cleared cookie: ${name}`)
        }
      })
    } catch (e) {
      log(`✗ Cookie clear failed: ${e}`)
    }
    
    setCookies(document.cookie || '(none)')
    log('✅ NUKE COMPLETE - Refresh the page')
  }

  return (
    <div className="min-h-screen bg-black text-white p-8 font-mono">
      <h1 className="text-2xl mb-4">🔧 Auth Debug Page</h1>
      
      <div className="mb-6">
        <h2 className="text-lg mb-2 text-gray-400">Cookies:</h2>
        <pre className="bg-gray-900 p-3 rounded text-xs overflow-x-auto max-w-full">
          {cookies}
        </pre>
      </div>
      
      <div className="flex gap-4 mb-6">
        <button
          onClick={checkAuth}
          className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-500"
        >
          Check Auth State
        </button>
        
        <button
          onClick={nukeEverything}
          className="px-4 py-2 bg-red-600 rounded hover:bg-red-500"
        >
          🔥 Nuke All Auth
        </button>
        
        <a
          href="/login"
          className="px-4 py-2 bg-green-600 rounded hover:bg-green-500"
        >
          → Go to Login
        </a>
      </div>
      
      <div>
        <h2 className="text-lg mb-2 text-gray-400">Log:</h2>
        <div className="bg-gray-900 p-3 rounded h-96 overflow-y-auto">
          {status.length === 0 ? (
            <p className="text-gray-500">Click a button to start...</p>
          ) : (
            status.map((line, i) => (
              <div key={i} className="text-xs mb-1">
                {line}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
