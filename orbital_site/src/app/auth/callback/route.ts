import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { NextResponse, type NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  // Note: 'next' param could be used for custom redirect destinations in future
  const _next = searchParams.get('next') ?? '/dashboard'
  const error = searchParams.get('error')
  const errorDescription = searchParams.get('error_description')

  console.log('Auth callback hit:', { code: !!code, error, origin })

  // Helper to create redirect with no-cache headers
  const safeRedirect = (url: string) => {
    const res = NextResponse.redirect(url)
    res.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate')
    res.headers.set('Pragma', 'no-cache')
    res.headers.set('Expires', '0')
    return res
  }

  // Handle OAuth errors from provider
  if (error) {
    console.error('OAuth error:', error, errorDescription)
    return safeRedirect(`${origin}/login?error=${encodeURIComponent(error)}`)
  }

  if (!code) {
    console.error('No code provided in callback')
    return safeRedirect(`${origin}/login?error=no_code`)
  }

  const cookieStore = await cookies()
  
  // Create a response that we'll add cookies to
  // Redirect to /auth/complete which handles client-side session finalization
  const redirectUrl = new URL('/auth/complete', origin)
  const response = NextResponse.redirect(redirectUrl)

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          // Set cookies on BOTH the cookie store AND the response
          // The response cookies are what get sent to the browser
          cookiesToSet.forEach(({ name, value, options }) => {
            // Set on cookie store (for server-side reads)
            try {
              cookieStore.set(name, value, options)
            } catch {
              // Ignore errors from cookie store in route handler
            }
            // Set on response (for browser)
            response.cookies.set(name, value, options)
          })
        },
      },
    }
  )

  // Exchange the code for a session
  const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code)

  if (exchangeError) {
    console.error('Code exchange error:', exchangeError.message)
    return safeRedirect(
      `${origin}/login?error=exchange_failed&message=${encodeURIComponent(exchangeError.message)}`
    )
  }

  // Verify we actually got a user (validates with Supabase Auth server)
  const { data: { user }, error: userError } = await supabase.auth.getUser()

  if (userError || !user) {
    console.error('User verification failed:', userError?.message)
    return safeRedirect(`${origin}/login?error=verification_failed`)
  }

  console.log('Session created for user:', user.email)

  // Add cache control headers to prevent browser caching issues
  response.headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate')
  response.headers.set('Pragma', 'no-cache')
  response.headers.set('Expires', '0')

  // Return the response with cookies - redirects to /auth/complete
  return response
}
