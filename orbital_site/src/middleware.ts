import { type NextRequest, NextResponse } from 'next/server'
import { updateSession } from '@/lib/supabase/middleware'

export async function middleware(request: NextRequest) {
  try {
    // Update session (refresh if needed) and get user
    const { supabaseResponse, user } = await updateSession(request)

    // Protected routes that require authentication
    const protectedPaths = ['/dashboard', '/settings', '/purchases', '/videos']
    const isProtectedRoute = protectedPaths.some(path => 
      request.nextUrl.pathname.startsWith(path)
    )

    // Auth routes (redirect to dashboard if already logged in)
    const authPaths = ['/login', '/signup']
    const isAuthRoute = authPaths.some(path => 
      request.nextUrl.pathname.startsWith(path)
    )

    // If accessing protected route without user, redirect to login
    if (isProtectedRoute && !user) {
      const redirectUrl = new URL('/login', request.url)
      redirectUrl.searchParams.set('redirect', request.nextUrl.pathname)
      return NextResponse.redirect(redirectUrl)
    }

    // If accessing auth routes while logged in, redirect to dashboard
    if (isAuthRoute && user) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }

    // IMPORTANT: Return the supabaseResponse to persist refreshed cookies
    return supabaseResponse
  } catch (e) {
    // If there's an error (corrupted cookies, network issues, etc.),
    // let the request through - the page can handle auth state
    console.error('Middleware error:', e)
    return NextResponse.next({
      request,
    })
  }
}

// Configure which routes use middleware
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
